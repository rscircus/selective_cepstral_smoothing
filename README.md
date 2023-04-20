# A Priori SNR Estimation and Optimization based on Selective Cepstral Smoothing

This is probably the most compact implementation of Selective Cepstro-Temporal Smoothing with an optimizer around it to find the perfect tuning for a given noisy speech signal.

_This approach displayed here goes one step further compared to the initial paper (see bottom) and optimizes for optimal SCTS settings using the L-BFGS-B algorithm._

## Method

"Selective Cepstro-Temporal Smoothing" (SCTS) consists of two stages:

1. Calculation of the Cepstrum: In the first stage, the cepstrum of the noisy speech signal is calculated. The cepstrum is a representation of the speech signal in the frequency domain that is obtained by acquiring the real values of the inverse Fourier transform of the logarithm of the magnitude of the Fourier transform of the speech signal.

2. Smoothing of the Cepstrum: In the second stage, the cepstrum is smoothed selectively in both the cepstral and temporal domains to obtain a more reliable estimate of the SNR.

We add a third stage optimizing for the ideal control given a noisy speech signal.

## References

> Colin Breithaupt, Timo Gerkmann, Rainer Martin, "A Novel A Priori SNR
> Estimation Approach Based on Selective Cepstro-Temporal Smoothing", IEEE
> Int. Conf. Acoustics, Speech, Signal Processing, Las Vegas, NV, USA,
> Apr. 2008.
