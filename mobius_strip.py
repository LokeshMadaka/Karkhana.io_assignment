import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MobiusStrip:
    def __init__(self, R=5, w=2, n=100):
        self.R = R
        self.w = w
        self.n = n
        self.u = np.linspace(0, 2 * np.pi, n)
        self.v = np.linspace(-w / 2, w / 2, n)
        self.U, self.V = np.meshgrid(self.u, self.v)
        self.X, self.Y, self.Z = self._compute_mesh()

    def _compute_mesh(self):
        U, V = self.U, self.V
        R = self.R
        X = (R + V * np.cos(U / 2)) * np.cos(U)
        Y = (R + V * np.cos(U / 2)) * np.sin(U)
        Z = V * np.sin(U / 2)
        return X, Y, Z

    def compute_surface_area(self):
        du = (2 * np.pi) / (self.n - 1)
        dv = self.w / (self.n - 1)
        U, V = self.U, self.V
        R = self.R
        Xu = (- (R + V * np.cos(U / 2)) * np.sin(U) - V * 0.5 * np.sin(U / 2) * np.cos(U))
        Yu = ((R + V * np.cos(U / 2)) * np.cos(U) - V * 0.5 * np.sin(U / 2) * np.sin(U))
        Zu = 0.5 * V * np.cos(U / 2)
        Xv = np.cos(U / 2) * np.cos(U)
        Yv = np.cos(U / 2) * np.sin(U)
        Zv = np.sin(U / 2)
        cross_mag = np.sqrt(
            (Yu * Zv - Zu * Yv) ** 2 +
            (Zu * Xv - Xu * Zv) ** 2 +
            (Xu * Yv - Yu * Xv) ** 2
        )
        area = np.sum(cross_mag) * du * dv
        return area

    def compute_edge_length(self):
        u = self.u
        v_edge = self.w / 2
        R = self.R
        dx_du = (- (R + v_edge * np.cos(u / 2)) * np.sin(u) - v_edge * 0.5 * np.sin(u / 2) * np.cos(u))
        dy_du = ((R + v_edge * np.cos(u / 2)) * np.cos(u) - v_edge * 0.5 * np.sin(u / 2) * np.sin(u))
        dz_du = 0.5 * v_edge * np.cos(u / 2)
        integrand = np.sqrt(dx_du ** 2 + dy_du ** 2 + dz_du ** 2)
        du = (2 * np.pi) / (self.n - 1)
        edge_length = np.sum(integrand) * du
        return edge_length

    def plot(self):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(
            self.X, self.Y, self.Z,
            rstride=1, cstride=1,
            facecolors=plt.cm.plasma((self.U % (2 * np.pi)) / (2 * np.pi)),
            linewidth=0, antialiased=True, alpha=0.95
        )
        ax.set_title("3D Möbius Strip Visualization", fontsize=16, weight='bold')
        ax.set_xlabel("X-axis", fontsize=12)
        ax.set_ylabel("Y-axis", fontsize=12)
        ax.set_zlabel("Z-axis", fontsize=12)
        ax.set_box_aspect([1, 1, 0.5])
        ax.grid(False)
        mappable = plt.cm.ScalarMappable(cmap='plasma')
        mappable.set_array(self.U)
        fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=10, label='U Parameter')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    mobius = MobiusStrip(R=5, w=2, n=300)
    area = mobius.compute_surface_area()
    edge_len = mobius.compute_edge_length()
    print(f"Approximate Surface Area: {area:.4f}")
    print(f"Approximate Edge Length: {edge_len:.4f}")
    mobius.plot()