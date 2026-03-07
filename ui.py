import pygame

CELL = 100

BG_COLOR = (240, 242, 247)

GRID_COLOR = (210, 210, 210)

PIPE_COLOR = (52, 152, 219)
PIPE_SHADOW = (41, 128, 185)

CELL_BG = (255, 255, 255)

HIGHLIGHT = (255, 180, 90)

PANEL_BG = (225, 228, 235)

TEXT = (40, 40, 40)


def draw_pipe(screen, pipe, x, y):

    rect = pygame.Rect(x, y, CELL, CELL)

    pygame.draw.rect(screen, CELL_BG, rect, border_radius=6)
    pygame.draw.rect(screen, GRID_COLOR, rect, 1, border_radius=6)

    center = (x + CELL // 2, y + CELL // 2)

    outer_thickness = CELL // 7
    inner_thickness = CELL // 13

    pygame.draw.circle(screen, PIPE_SHADOW, center, outer_thickness // 2)
    pygame.draw.circle(screen, CELL_BG, center, inner_thickness // 2)

    for direction in pipe.get_connections():

        if direction == 0:  # up
            end = (center[0], y)

        elif direction == 1:  # right
            end = (x + CELL, center[1])

        elif direction == 2:  # down
            end = (center[0], y + CELL)

        elif direction == 3:  # left
            end = (x, center[1])

        pygame.draw.line(
            screen,
            PIPE_SHADOW,
            center,
            end,
            outer_thickness
        )

        pygame.draw.line(
            screen,
            CELL_BG,
            center,
            end,
            inner_thickness
        )


def draw_grid(screen, font, small_font, grid, highlight, status, autoplay):

    screen.fill(BG_COLOR)

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    grid_width = grid.cols * CELL
    grid_height = grid.rows * CELL

    start_x = (screen_width - grid_width) // 2
    start_y = (screen_height - grid_height - 140) // 2

    # grid shadow
    shadow_rect = pygame.Rect(
        start_x - 6,
        start_y - 6,
        grid_width + 12,
        grid_height + 12
    )

    pygame.draw.rect(screen, (200, 200, 200),
                     shadow_rect,
                     border_radius=8)

    # draw pipes
    for r in range(grid.rows):
        for c in range(grid.cols):

            x = start_x + c * CELL
            y = start_y + r * CELL

            draw_pipe(screen, grid.grid[r][c], x, y)

    # highlight current cell
    if highlight:

        r, c = highlight

        x = start_x + c * CELL
        y = start_y + r * CELL

        pygame.draw.rect(
            screen,
            HIGHLIGHT,
            (x - 2, y - 2, CELL + 4, CELL + 4),
            3,
            border_radius=6
        )

    # panel
    panel_y = start_y + grid_height + 20

    panel_rect = pygame.Rect(
        40,
        panel_y,
        screen_width - 80,
        110
    )

    pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=8)
    pygame.draw.rect(screen, GRID_COLOR, panel_rect, 1, border_radius=8)

    instructions = "→ Next   ← Back   ENTER AutoPlay   ESC Quit"

    inst_surface = small_font.render(instructions, True, TEXT)

    screen.blit(
        inst_surface,
        (
            panel_rect.centerx - inst_surface.get_width() // 2,
            panel_y + 10
        )
    )

    auto_text = f"Autoplay: {'ON' if autoplay else 'OFF'}"

    auto_surface = small_font.render(auto_text, True, TEXT)

    screen.blit(
        auto_surface,
        (
            panel_rect.centerx - auto_surface.get_width() // 2,
            panel_y + 40
        )
    )

    status_surface = font.render(status, True, TEXT)

    screen.blit(
        status_surface,
        (
            panel_rect.centerx - status_surface.get_width() // 2,
            panel_y + 70
        )
    )

    pygame.display.flip()


def replay_steps(steps):

    pygame.init()

    width = 1000
    height = 850

    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption("DFS Pipes Visualization")

    font = pygame.font.SysFont("consolas", 26, bold=True)
    small_font = pygame.font.SysFont("consolas", 18)

    clock = pygame.time.Clock()

    idx = 0
    autoplay = False

    while True:

        clock.tick(60)

        grid, pos, action, rot = steps[idx]

        if action == "try":
            status = f"🔄 TRY rotation {rot}"

        elif action == "backtrack":
            status = f"⤺ BACKTRACK"

        elif action == "done":
            status = f"✔ SOLVED"

        else:
            status = f"[{idx+1}/{len(steps)}]"

        draw_grid(
            screen,
            font,
            small_font,
            grid,
            pos,
            status,
            autoplay
        )

        if autoplay:

            pygame.time.delay(150)

            if idx < len(steps) - 1:
                idx += 1
            else:
                autoplay = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                if event.key == pygame.K_RIGHT:
                    if idx < len(steps) - 1:
                        idx += 1

                if event.key == pygame.K_LEFT:
                    if idx > 0:
                        idx -= 1

                if event.key == pygame.K_RETURN:
                    autoplay = not autoplay