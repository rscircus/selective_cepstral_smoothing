# This project implements
# A novel a priori SNR estimation approach based on selective cepstro-temporal smoothing.
import numpy as np
from scipy.signal import lfilter
from scipy.optimize import minimize


def calculate_scts(noisy_signal, t_smooth=5, t_step=1, t_win_len=20, c_smooth=5, c_step=1, c_win_len=10):
    # Calculate the cepstrum of the noisy signal
    noisy_fft = np.fft.fft(noisy_signal)
    log_mag = np.log(np.abs(noisy_fft))
    cepstrum = np.real(np.fft.ifft(log_mag))

    # Temporal smoothing of cepstrum
    t_smooth_kernel = np.ones(t_win_len) / t_win_len
    smooth_cepstrum = np.zeros_like(cepstrum)
    for t in range(cepstrum.shape[1]):
        start_t = max(0, t-t_step)
        end_t = min(cepstrum.shape[1], t+t_step+1)
        temp_cepstrum = cepstrum[:, start_t:end_t]
        temp_cepstrum = lfilter(t_smooth_kernel, 1, temp_cepstrum, axis=1)
        smooth_cepstrum[:, t] = temp_cepstrum[:, t_step]

    # Cepstral smoothing of the smoothed cepstrum
    c_smooth_kernel = np.ones(c_win_len) / c_win_len
    scts_cepstrum = np.zeros_like(smooth_cepstrum)
    for c in range(smooth_cepstrum.shape[0]):
        start_c = max(0, c-c_step)
        end_c = min(smooth_cepstrum.shape[0], c+c_step+1)
        temp_cepstrum = smooth_cepstrum[start_c:end_c, :]
        temp_cepstrum = lfilter(c_smooth_kernel, 1, temp_cepstrum, axis=0)
        scts_cepstrum[c, :] = temp_cepstrum[c_step, :]

    # Estimate the noise spectrum
    scts_cepstrum = np.exp(scts_cepstrum)
    noise_spectrum = np.mean(np.abs(np.fft.fft(scts_cepstrum))**2, axis=1)
    signal_power = np.mean(np.abs(noisy_fft)**2)
    noise_power = np.sum(noise_spectrum)
    snr = signal_power / noise_power

    return snr


# TODO: The noisy signal actually is the main influence
#       for how good the SNR will be.
# TODO: Ideas:
#       - Test for different languages,
#       - and different noise levels.
#
def optimize_scts(noisy_signal):
    # Define the objective function to be minimized
    def objective(x):
        t_smooth, t_step, t_win_len, c_smooth, c_step, c_win_len = x
        snr = calculate_scts(noisy_signal,
                             t_smooth=t_smooth,
                             t_step=t_step,
                             t_win_len=t_win_len,
                             c_smooth=c_smooth,
                             c_step=c_step,
                             c_win_len=c_win_len)
        return -snr  # We want to maximize SNR, so minimize its negative

    # Define the initial guess for the SCTS parameters
    # TODO: Find good initial guess
    x0 = [5, 1, 20, 5, 1, 10]

    # Define the bounds for the SCTS parameters
    # TODO: Find good bounds
    bounds = [(1, 20), (1, 10), (10, 50), (1, 20), (1, 10), (5, 20)]

    # Minimize the objective function using
    # the L-BFGS-B algorithm, because it was already
    # awesome during my PhD thesis. 🙂
    return minimize(objective, x0, bounds=bounds, method='L-BFGS-B')


# TODO: Train
ret = optimize_scts(None)
print(ret)
