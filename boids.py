"""Basic boids simulation using tkinter (no extra dependencies)."""
import math
import random
import tkinter as tk

WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 60
MAX_SPEED = 4.0
VIEW_RADIUS = 50
SEP_RADIUS = 20
COHESION, ALIGNMENT, SEPARATION = 0.005, 0.05, 0.1


class Boid:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        a = random.uniform(0, 2 * math.pi)
        self.vx, self.vy = math.cos(a) * MAX_SPEED, math.sin(a) * MAX_SPEED


def step(boids):
    for b in boids:
        cx = cy = ax = ay = sx = sy = 0.0
        n = 0
        for o in boids:
            if o is b:
                continue
            dx, dy = o.x - b.x, o.y - b.y
            d = math.hypot(dx, dy)
            if d < VIEW_RADIUS:
                cx += o.x; cy += o.y
                ax += o.vx; ay += o.vy
                n += 1
                if d < SEP_RADIUS:
                    sx -= dx; sy -= dy
        if n:
            b.vx += (cx / n - b.x) * COHESION + (ax / n - b.vx) * ALIGNMENT
            b.vy += (cy / n - b.y) * COHESION + (ay / n - b.vy) * ALIGNMENT
        b.vx += sx * SEPARATION
        b.vy += sy * SEPARATION
        speed = math.hypot(b.vx, b.vy)
        if speed > MAX_SPEED:
            b.vx, b.vy = b.vx / speed * MAX_SPEED, b.vy / speed * MAX_SPEED
    for b in boids:
        b.x = (b.x + b.vx) % WIDTH
        b.y = (b.y + b.vy) % HEIGHT


def draw(canvas, boids):
    canvas.delete("all")
    for b in boids:
        a = math.atan2(b.vy, b.vx)
        pts = [
            b.x + math.cos(a) * 8, b.y + math.sin(a) * 8,
            b.x + math.cos(a + 2.5) * 5, b.y + math.sin(a + 2.5) * 5,
            b.x + math.cos(a - 2.5) * 5, b.y + math.sin(a - 2.5) * 5,
        ]
        canvas.create_polygon(pts, fill="white")


def main():
    root = tk.Tk()
    root.title("Boids")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()
    boids = [Boid() for _ in range(NUM_BOIDS)]

    def tick():
        step(boids)
        draw(canvas, boids)
        root.after(16, tick)

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
