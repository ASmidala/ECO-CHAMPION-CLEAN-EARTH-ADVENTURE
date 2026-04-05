import pygame
import sys
import random
import math


class CheapGreenPower:
    def __init__(self):
        pygame.init()
        # Responsive Setup
        info = pygame.display.Info()
        self.W = info.current_w if info.current_w > 0 else 1024
        self.H = info.current_h if info.current_h > 0 else 600

        self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
        pygame.display.set_caption("Cheap Green Power - SEDC")
        self.clock = pygame.time.Clock()

        self.u = self.W / 100  # Responsive Unit

        self.state = 'CRISIS'
        self.points = 0
        self.revenue = 0
        self.target_points = 1000
        self.timer = 0

        self.deforestation, self.aqi, self.charcoal_usage = 85.0, 180, 94.0

        # Fonts
        self.title_font = pygame.font.SysFont("Verdana", int(self.u * 4.0), bold=True)
        self.stat_font = pygame.font.SysFont("Consolas", int(self.u * 1.6), bold=True)
        self.cert_font = pygame.font.SysFont("Georgia", int(self.u * 2.5), italic=True)
        self.credit_font = pygame.font.SysFont("Arial", int(self.u * 1.3), bold=True)

        self.items = {
            "Rice Husk": (210, 180, 140), "Coffee": (75, 54, 33),
            "Dusa": (245, 222, 179), "Plastic": (0, 0, 255)
        }
        self.prices = {"Rice Husk": 500, "Coffee": 400, "Dusa": 200, "Plastic": -1000}

        self.mtn_pts = self.gen_mtn()
        self.smoke = [[random.randint(0, self.W), random.randint(0, self.H), random.uniform(1, 3)] for _ in range(50)]
        self.clouds = [[random.randint(0, self.W), random.randint(50, 150), random.uniform(0.5, 1.2)] for _ in range(5)]

        self.item_pos = {}
        self.dragging = None
        self.machine_rect = pygame.Rect(self.W // 2 - (10 * self.u), self.H // 2 + (5 * self.u), 20 * self.u,
                                        10 * self.u)
        self.reset_items()

    def gen_mtn(self):
        return [(0, self.H * 0.8), (self.W * 0.2, self.H * 0.6), (self.W * 0.4, self.H * 0.75),
                (self.W * 0.6, self.H * 0.55), (self.W * 0.8, self.H * 0.7), (self.W, self.H * 0.8), (self.W, self.H),
                (0, self.H)]

    def reset_items(self):
        for i, k in enumerate(self.items.keys()):
            self.item_pos[k] = [self.W // 5 * (i + 1) - (3 * self.u), self.H * 0.15]

    def draw_dashboard(self, x, y):
        s = pygame.Surface((28 * self.u, 14 * self.u), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (x, y))
        color = (255, 100, 100) if self.aqi > 100 else (100, 255, 100)
        self.screen.blit(self.stat_font.render("DATA DASHBOARD", True, color), (x + self.u, y + self.u))
        self.screen.blit(self.stat_font.render(f"DEFORESTATION: {self.deforestation:.1f}%", True, (255, 255, 255)),
                         (x + self.u, y + 4 * self.u))
        self.screen.blit(self.stat_font.render(f"AIR QUALITY: {self.aqi} AQI", True, (255, 255, 255)),
                         (x + self.u, y + 7 * self.u))
        self.screen.blit(self.stat_font.render(f"CHARCOAL: {self.charcoal_usage:.1f}%", True, (255, 255, 255)),
                         (x + self.u, y + 10 * self.u))

    def draw_certificate(self):
        c_w, c_h = self.W * 0.9, self.H * 0.85
        overlay = pygame.Surface((c_w, c_h))
        overlay.fill((255, 253, 240))
        pygame.draw.rect(overlay, (34, 139, 34), (0, 0, c_w, c_h), int(self.u))

        # 1. Title
        title = self.title_font.render("CHEAP GREEN POWER AMBASSADOR", True, (34, 139, 34))
        # 2. Honors
        honors = self.cert_font.render("Certified Gombe Green Impact Leader", True, (0, 0, 0))
        # 3. Developer Credit (Your Name)
        dev_name = self.credit_font.render("Developed by: Abubakar Saidu Midala (Mysterious Global Tech)", True,
                                           (50, 50, 50))
        # 4. Economic Result
        revenue_val = self.stat_font.render(f"Total Revenue Generated: ₦{self.revenue}", True, (0, 100, 0))
        # 5. Copyright
        copyright_txt = self.stat_font.render("© 2026 QS ImpACT Gombe Team", True, (100, 100, 100))

        # Blit with vertical spacing to prevent overlap
        overlay.blit(title, (c_w // 2 - title.get_width() // 2, c_h * 0.15))
        overlay.blit(honors, (c_w // 2 - honors.get_width() // 2, c_h * 0.35))
        overlay.blit(dev_name, (c_w // 2 - dev_name.get_width() // 2, c_h * 0.55))
        overlay.blit(revenue_val, (c_w // 2 - revenue_val.get_width() // 2, c_h * 0.70))
        overlay.blit(copyright_txt, (c_w // 2 - copyright_txt.get_width() // 2, c_h * 0.85))

        self.screen.blit(overlay, (self.W // 2 - c_w // 2, self.H // 2 - c_h // 2))

    def run(self):
        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.W, self.H = event.w, event.h
                    self.u = self.W / 100
                    self.machine_rect = pygame.Rect(self.W // 2 - (10 * self.u), self.H // 2 + (5 * self.u),
                                                    20 * self.u, 10 * self.u)
                    self.mtn_pts = self.gen_mtn()

                if self.state == 'CRISIS' and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: self.state = 'CHALLENGE'

                if self.state == 'CHALLENGE':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for name, pos in self.item_pos.items():
                            if pygame.Rect(pos[0], pos[1], 6 * self.u, 6 * self.u).collidepoint(event.pos):
                                self.dragging = name
                    if event.type == pygame.MOUSEBUTTONUP and self.dragging:
                        if self.machine_rect.collidepoint(event.pos):
                            val = self.prices[self.dragging]
                            self.revenue += max(0, val)
                            self.points = min(self.target_points, max(0, self.points + (250 if val > 0 else -400)))
                            if val > 0:
                                self.deforestation = max(12, self.deforestation - 15)
                                self.aqi = max(42, self.aqi - 30)
                                self.charcoal_usage = max(15, self.charcoal_usage - 18)
                        self.reset_items();
                        self.dragging = None
                        if self.points >= self.target_points:
                            self.state = 'SUCCESS';
                            self.timer = pygame.time.get_ticks()

                if self.state in ['CERT', 'SUCCESS'] and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.points, self.revenue = 0, 0
                        self.deforestation, self.aqi, self.charcoal_usage = 85.0, 180, 94.0
                        self.state = 'CHALLENGE'
                    if event.key == pygame.K_q: pygame.quit(); sys.exit()

            # Drawing
            if self.state == 'CRISIS':
                self.screen.fill((50, 45, 40))
                for p in self.smoke:
                    p[1] -= p[2]
                    pygame.draw.circle(self.screen, (80, 80, 80), (int(p[0]), int(p[1])), int(self.u))
                    if p[1] < 0: p[1] = self.H
                pygame.draw.polygon(self.screen, (20, 20, 20), self.mtn_pts)
                t = self.title_font.render("CHEAP GREEN POWER", True, (255, 50, 50))
                self.screen.blit(t, (self.W // 2 - t.get_width() // 2, self.H // 2 - 2 * self.u))
                self.draw_dashboard(self.u * 2, self.u * 2)

            elif self.state == 'CHALLENGE':
                self.screen.fill((100, 105, 110))
                pygame.draw.rect(self.screen, (150, 150, 150), self.machine_rect, border_radius=12)
                self.draw_dashboard(self.u * 2, self.H - 16 * self.u)
                for name, color in self.items.items():
                    pos = self.item_pos[name]
                    if self.dragging == name: pos = [mx - (3 * self.u), my - (3 * self.u)]
                    pygame.draw.rect(self.screen, color, (pos[0], pos[1], 6 * self.u, 6 * self.u), border_radius=8)
                    self.screen.blit(self.stat_font.render(name, True, (255, 255, 255)), (pos[0], pos[1] - 2 * self.u))
                pygame.draw.rect(self.screen, (50, 50, 50),
                                 (self.W // 2 - 15 * self.u, 3 * self.u, 30 * self.u, 2 * self.u))
                pygame.draw.rect(self.screen, (0, 255, 100), (
                self.W // 2 - 15 * self.u, 3 * self.u, (self.points / 1000) * 30 * self.u, 2 * self.u))

            elif self.state == 'SUCCESS':
                self.screen.fill((135, 206, 235))
                for c in self.clouds:
                    c[0] += c[2];
                    pygame.draw.circle(self.screen, (255, 255, 255), (int(c[0]), int(c[1])), 30)
                    if c[0] > self.W: c[0] = -100
                pygame.draw.polygon(self.screen, (34, 139, 34), self.mtn_pts)
                v = self.title_font.render("GOMBE RESTORED!", True, (255, 255, 255))
                self.screen.blit(v, (self.W // 2 - v.get_width() // 2, self.H // 2))
                if pygame.time.get_ticks() - self.timer > 3000: self.state = 'CERT'

            elif self.state == 'CERT':
                self.screen.fill((135, 206, 235))
                pygame.draw.polygon(self.screen, (34, 139, 34), self.mtn_pts)
                self.draw_certificate()

            pygame.display.flip();
            self.clock.tick(60)


if __name__ == "__main__":
    CheapGreenPower().run()