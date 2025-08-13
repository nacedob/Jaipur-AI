# pygame_gui.py
import pygame
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass
from ..core import Card
from .basegui import BaseGUI
from .views import PlayerView, MarketView

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
BROWN = (165, 42, 42)
RED = (255, 0, 0)
BEIGE = (245, 245, 220)

# Card colors
CARD_COLORS = {
    Card.DIAMOND: (0, 191, 255),
    Card.GOLD: GOLD,
    Card.SILVER: SILVER,
    Card.CLOTH: WHITE,
    Card.SPICE: RED,
    Card.LEATHER: BROWN,
    Card.CAMEL: (210, 180, 140)
}



class PygameGUI:
    def __init__(self):
        pygame.init()
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Jaipur")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 22)
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.button_color = (70, 130, 180)
        self.button_hover = (100, 150, 200)

        # Load card images or create placeholders
        self.card_images = self._create_card_placeholders()

    def _create_card_placeholders(self):
        """Create simple colored rectangles as card placeholders"""
        card_images = {}
        for card in Card:
            surf = pygame.Surface((80, 120))
            surf.fill(CARD_COLORS[card])
            pygame.draw.rect(surf, BLACK, surf.get_rect(), 2)

            # Add card name
            text = self.font.render(card.name[:5], True, BLACK)
            text_rect = text.get_rect(center=(40, 60))
            surf.blit(text, text_rect)

            card_images[card] = surf
        return card_images

    def _draw_button(self, text, rect, hover=False):
        color = self.button_hover if hover else self.button_color
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=5)

        text_surf = self.font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        return rect

    def show_game_state(self, players: List[PlayerView], market: MarketView):
        self.screen.fill(BEIGE)

        # Draw title
        title = self.title_font.render("JAIPUR", True, BLACK)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 20))

        # Draw market
        self._draw_market(market)

        # Draw players
        for i, player in enumerate(players):
            self._draw_player(player, i)

        pygame.display.flip()

    def _draw_market(self, market: MarketView):
        # Market title
        market_title = self.font.render("MARKET", True, BLACK)
        self.screen.blit(market_title, (50, 80))

        # Draw goods
        x, y = 50, 120
        for card, count in market.goods.items():
            if count > 0:
                for _ in range(count):
                    self.screen.blit(self.card_images[card], (x, y))
                    x += 90
        for _ in range(market.camels):
            self.screen.blit(self.card_images[Card.CAMEL], (x, y))
            x += 90

    def _draw_player(self, player: PlayerView, player_num: int):
        y_offset = 300 if player_num == 0 else 500
        player_title = self.font.render(player.name, True, BLACK)
        self.screen.blit(player_title, (50, y_offset))

        # Draw hand
        x, y = 50, y_offset + 40
        for card, count in player.hand.items():
            if count > 0:
                for _ in range(count):
                    self.screen.blit(self.card_images[card], (x, y))
                    x += 90

        # Draw camels and tokens
        camel_text = self.font.render(f"Camels: {player.camels}", True, BLACK)
        self.screen.blit(camel_text, (50, y_offset + 180))

        token_text = self.font.render(f"Tokens: {player.tokens}", True, BLACK)
        self.screen.blit(token_text, (200, y_offset + 180))

    def show_turn_options(self):
        buttons = [
            ("Take Good", pygame.Rect(700, 100, 200, 50)),
            ("Take Camels", pygame.Rect(700, 170, 200, 50)),
            ("Sell Goods", pygame.Rect(700, 240, 200, 50)),
            ("Exchange", pygame.Rect(700, 310, 200, 50)),
            ("View State", pygame.Rect(700, 380, 200, 50))
        ]

        mouse_pos = pygame.mouse.get_pos()
        for text, rect in buttons:
            hover = rect.collidepoint(mouse_pos)
            self._draw_button(text, rect, hover)

        pygame.display.flip()
        return buttons

    def get_action_choice(self) -> Optional[int]:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = self.show_turn_options()  # Redraw to get button rects
                    mouse_pos = pygame.mouse.get_pos()

                    for i, (_, rect) in enumerate(buttons, 1):
                        if rect.collidepoint(mouse_pos):
                            return i
            self.clock.tick(30)

    def select_good(self, available_goods: List[Card]) -> Optional[Card]:
        if not available_goods:
            return None

        self.screen.fill(BEIGE)
        title = self.font.render("Select a good to take:", True, BLACK)
        self.screen.blit(title, (50, 50))

        cards_rects = []
        x, y = 50, 100
        for i, card in enumerate(available_goods):
            rect = pygame.Rect(x, y, 100, 150)
            cards_rects.append((card, rect))

            pygame.draw.rect(self.screen, WHITE, rect, border_radius=5)
            pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=5)

            # Draw card
            self.screen.blit(self.card_images[card], (x + 10, y + 10))

            x += 120
            if x > self.screen_width - 120:
                x = 50
                y += 170

        # Cancel button
        cancel_rect = pygame.Rect(self.screen_width // 2 - 100, y + 100, 200, 50)
        self._draw_button("Cancel", cancel_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if cancel_rect.collidepoint(mouse_pos):
                        return None

                    for card, rect in cards_rects:
                        if rect.collidepoint(mouse_pos):
                            return card
            self.clock.tick(30)

    def show_message(self, message: str):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # Draw message box
        box_width = 600
        box_height = 200
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2

        pygame.draw.rect(self.screen, WHITE, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, BLACK, (box_x, box_y, box_width, box_height), 2)

        # Render message text (with word wrapping)
        words = message.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = self.font.size(test_line)[0]

            if test_width < box_width - 40:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Draw lines
        y_offset = box_y + 30
        for line in lines:
            text = self.font.render(line, True, BLACK)
            self.screen.blit(text, (box_x + 20, y_offset))
            y_offset += 30

        # Draw OK button
        ok_rect = pygame.Rect(self.screen_width // 2 - 50, box_y + box_height - 70, 100, 40)
        self._draw_button("OK", ok_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if ok_rect.collidepoint(mouse_pos):
                        return
            self.clock.tick(30)

    def show_error(self, error: str):
        self.show_message(f"ERROR: {error}")

    def cleanup(self):
        pygame.quit()