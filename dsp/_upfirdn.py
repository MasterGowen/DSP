# Code adapted from "upfirdn" python library with permission:
#
# Copyright (c) 2009, Motorola, Inc
#
# All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# * Neither the name of Motorola nor the names of its contributors may be
# used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
import pyximport; pyximport.install()
from ._upfirdn_apply import _output_len, _apply

__all__ = ['upfirdn', '_output_len']


def _pad_h(h, up):
    """Store coefficients in a transposed, flipped arrangement.

    For example, suppose upRate is 3, and the
    input number of coefficients is 10, represented as h[0], ..., h[9].

    Then the internal buffer will look like this::

       h[9], h[6], h[3], h[0],   // flipped phase 0 coefs
       0,    h[7], h[4], h[1],   // flipped phase 1 coefs (zero-padded)
       0,    h[8], h[5], h[2],   // flipped phase 2 coefs (zero-padded)

    """
    h_padlen = len(h) + (-len(h) % up)
    h_full = np.zeros(h_padlen, h.dtype)
    h_full[:len(h)] = h
    h_full = h_full.reshape(-1, up).T[:, ::-1].ravel()
    return h_full


class _UpFIRDn(object):
    def __init__(self, h, x_dtype, up, down):
        """Helper for resampling"""
        h = np.asarray(h)
        if h.ndim != 1 or h.size == 0:
            raise ValueError('h must be 1D with non-zero length')
        self._output_type = np.result_type(h.dtype, x_dtype, np.float32)
        h = np.asarray(h, self._output_type)
        self._up = int(up)
        self._down = int(down)
        if self._up < 1 or self._down < 1:
            raise ValueError('Both up and down must be >= 1')
        # This both transposes, and "flips" each phase for filtering
        self._h_trans_flip = _pad_h(h, self._up)
        self._h_trans_flip = np.ascontiguousarray(self._h_trans_flip)

    def apply_filter(self, x, axis=-1):
        """Apply the prepared filter to the specified axis of a nD signal x"""
        output_len = _output_len(len(self._h_trans_flip), x.shape[axis],
                                 self._up, self._down)
        output_shape = np.asarray(x.shape)
        output_shape[axis] = output_len
        out = np.zeros(output_shape, dtype=self._output_type, order='C')
        axis = axis % x.ndim
        _apply(np.asarray(x, self._output_type),
               self._h_trans_flip, out,
               self._up, self._down, axis)
        return out


def upfirdn(h, x, up=1, down=1, axis=-1):
    """Upsample, FIR filter, and downsample

    Parameters
    ----------
    h : array_like
        1-dimensional FIR (finite-impulse response) filter coefficients.
    x : array_like
        Input signal array.
    up : int, optional
        Upsampling rate. Default is 1.
    down : int, optional
        Downsampling rate. Default is 1.
    axis : int, optional
        The axis of the input data array along which to apply the
        linear filter. The filter is applied to each subarray along
        this axis. Default is -1.

    Returns
    -------
    y : ndarray
        The output signal array. Dimensions will be the same as `x` except
        for along `axis`, which will change size according to the `h`,
        `up`,  and `down` parameters.

    Notes
    -----
    The algorithm is an implementation of the block diagram shown on page 129
    of the Vaidyanathan text [1]_ (Figure 4.3-8d).

    .. [1] P. P. Vaidyanathan, Multirate Systems and Filter Banks,
       Prentice Hall, 1993.

    The direct approach of upsampling by factor of P with zero insertion,
    FIR filtering of length ``N``, and downsampling by factor of Q is
    O(N*Q) per output sample. The polyphase implementation used here is
    O(N/P).

    .. versionadded:: 0.18

    Examples
    --------
    Simple operations:


    """
    x = np.asarray(x)
    ufd = _UpFIRDn(h, x.dtype, up, down)
    # This is equivalent to (but faster than) using np.apply_along_axis
    return ufd.apply_filter(x, axis)