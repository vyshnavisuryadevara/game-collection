from ursina import *

app = Ursina()
window.title = "Brick Breaker Game"
window.color = color.black


paddle = Entity(model='cube', color=color.azure, scale=(2, 0.4, 0), position=(0, -4), collider='box')


ball = Entity(model='sphere', color=color.white, scale=0.3, position=(0, -3.5), collider='box')
ball.velocity = Vec2(3, 4)


bricks = []
colors = [color.red, color.orange, color.green, color.yellow]

for y in range(4):
    for x in range(8):
        brick = Entity(
            model='cube',
            color=colors[y % len(colors)],
            scale=(1.6, 0.5, 0),
            position=(-6 + x * 1.7, 3 - y * 0.6),
            collider='box'
        )
        bricks.append(brick)


score = 0
score_text = Text(text=f"Score: {score}", position=(-0.85, 0.45), scale=2)


game_over_text = Text(text="Game Over!", origin=(0, 0), scale=3, enabled=False)

def update():
    global score

   
    if held_keys['left arrow']:
        paddle.x -= 5 * time.dt
    if held_keys['right arrow']:
        paddle.x += 5 * time.dt

    
    paddle.x = clamp(paddle.x, -6.5, 6.5)

    
    ball.x += ball.velocity.x * time.dt
    ball.y += ball.velocity.y * time.dt

    
    if abs(ball.x) > 7:
        ball.velocity.x *= -1
    if ball.y > 5:
        ball.velocity.y *= -1

    
    if ball.y < -5:
        ball.disable()
        game_over_text.enabled = True

    
    if ball.intersects(paddle).hit:
        ball.velocity.y *= -1
        ball.y = paddle.y + 0.3  
    
    for brick in bricks:
        if brick.enabled and ball.intersects(brick).hit:
            ball.velocity.y *= -1
            brick.disable()
            score += 1
            score_text.text = f"Score: {score}"
            break

app.run()