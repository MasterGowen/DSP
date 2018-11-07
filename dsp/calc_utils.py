import numpy as np
from scipy.signal.fir_filter_design import firwin
from scipy.signal._upfirdn import _output_len, _UpFIRDn


def arrays_is_equal(x, y):
    return np.array_equal(x, y)


def numbers_is_equal(x, y, tol=0.5, rel=0.00005):
    if tol is rel is None:
        raise TypeError('cannot specify both absolute and relative errors are None')
    tests = []
    if tol is not None: tests.append(tol)
    if rel is not None: tests.append(rel * abs(x))
    assert tests
    return abs(x - y) <= max(tests)


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def resample_poly(x, up, down, axis=0, window=('kaiser', 5.0)):
    """
    Resample `x` along the given axis using polyphase filtering.
    The signal `x` is upsampled by the factor `up`, a zero-phase low-pass
    FIR filter is applied, and then it is downsampled by the factor `down`.
    The resulting sample rate is ``up / down`` times the original sample
    rate. Values beyond the boundary of the signal are assumed to be zero
    during the filtering step.
    Parameters
    ----------
    x : array_like
        The data to be resampled.
    up : int
        The upsampling factor.
    down : int
        The downsampling factor.
    axis : int, optional
        The axis of `x` that is resampled. Default is 0.
    window : string, tuple, or array_like, optional
        Desired window to use to design the low-pass filter, or the FIR filter
        coefficients to employ. See below for details.
    Returns
    -------
    resampled_x : array
        The resampled array.
    See also
    --------
    decimate : Downsample the signal after applying an FIR or IIR filter.
    resample : Resample up or down using the FFT method.
    Notes
    -----
    This polyphase method will likely be faster than the Fourier method
    in `scipy.signal.resample` when the number of samples is large and
    prime, or when the number of samples is large and `up` and `down`
    share a large greatest common denominator. The length of the FIR
    filter used will depend on ``max(up, down) // gcd(up, down)``, and
    the number of operations during polyphase filtering will depend on
    the filter length and `down` (see `scipy.signal.upfirdn` for details).
    The argument `window` specifies the FIR low-pass filter design.
    If `window` is an array_like it is assumed to be the FIR filter
    coefficients. Note that the FIR filter is applied after the upsampling
    step, so it should be designed to operate on a signal at a sampling
    frequency higher than the original by a factor of `up//gcd(up, down)`.
    This function's output will be centered with respect to this array, so it
    is best to pass a symmetric filter with an odd number of samples if, as
    is usually the case, a zero-phase filter is desired.
    For any other type of `window`, the functions `scipy.signal.get_window`
    and `scipy.signal.firwin` are called to generate the appropriate filter
    coefficients.
    The first sample of the returned vector is the same as the first
    sample of the input vector. The spacing between samples is changed
    from ``dx`` to ``dx * up / float(down)``.
    Examples
    --------
    Note that the end of the resampled data rises to meet the first
    sample of the next cycle for the FFT method, and gets closer to zero
    for the polyphase method:
    # >>> from scipy import signal
    # >>> x = np.linspace(0, 10, 20, endpoint=False)
    # >>> y = np.cos(-x**2/6.0)
    # >>> f_fft = signal.resample(y, 100)
    # >>> f_poly = signal.resample_poly(y, 100, 20)
    # >>> xnew = np.linspace(0, 10, 100, endpoint=False)
    # >>> import matplotlib.pyplot as plt
    # >>> plt.plot(xnew, f_fft, 'b.-', xnew, f_poly, 'r.-')
    # >>> plt.plot(x, y, 'ko-')
    # >>> plt.plot(10, y[0], 'bo', 10, 0., 'ro')  # boundaries
    # >>> plt.legend(['resample', 'resamp_poly', 'data'], loc='best')
    # >>> plt.show()
    """
    x = np.asarray(x)
    up = int(up)
    down = int(down)
    if up < 1 or down < 1:
        raise ValueError('up and down must be >= 1')

    # Determine our up and down factors
    # Use a rational approimation to save computation time on really long
    # signals
    g_ = gcd(up, down)
    up //= g_
    down //= g_
    if up == down == 1:
        return x.copy()
    n_out = x.shape[axis] * up
    n_out = n_out // down + bool(n_out % down)

    if isinstance(window, (list, np.ndarray)):
        window = np.asarray(window)
        if window.ndim > 1:
            raise ValueError('window must be 1-D')
        half_len = (window.size - 1) // 2
        h = window
    else:
        # Design a linear-phase low-pass FIR filter
        max_rate = max(up, down)
        f_c = 1. / max_rate  # cutoff of FIR filter (rel. to Nyquist)
        half_len = 10 * max_rate  # reasonable cutoff for our sinc-like function
        h = firwin(2 * half_len + 1, f_c, window=window)
    h *= up

    # Zero-pad our filter to put the output samples at the center
    n_pre_pad = (down - half_len % down)
    n_post_pad = 0
    n_pre_remove = (half_len + n_pre_pad) // down
    # We should rarely need to do this given our filter lengths...
    while _output_len(len(h) + n_pre_pad + n_post_pad, x.shape[axis],
                      up, down) < n_out + n_pre_remove:
        n_post_pad += 1
    h = np.concatenate((np.zeros(n_pre_pad), h, np.zeros(n_post_pad)))
    ufd = _UpFIRDn(h, x.dtype, up, down)
    n_pre_remove_end = n_pre_remove + n_out

    def apply_remove(x):
        """Apply the upfirdn filter and remove excess"""
        return ufd.apply_filter(x)[n_pre_remove:n_pre_remove_end]

    y = np.apply_along_axis(apply_remove, axis, x)
    return y