import numpy as np

# Number of samplepoints
N = 600
# sample spacing
T = 1.0 / 600.0
x = np.linspace(0.0, N*T, N)
y = 3.0 + np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = np.fft.fft(y)

xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

for dx, dy in zip(xf,2.0/N*np.abs(yf[0:N/2])):
    print dx, dy


#plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))


