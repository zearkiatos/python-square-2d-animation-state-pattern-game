import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def create_square(world: esper.World, size: pygame.Vector2, position: pygame.Vector2, velocity: pygame.Vector2, color: pygame.Color) -> int:
    square_entity = world.create_entity()
    world.add_component(square_entity, CSurface(
        size, color))
    world.add_component(
        square_entity, CTransform(position))
    world.add_component(
        square_entity, CVelocity(velocity))

    return square_entity


def create_sprite(world: esper.World, position: pygame.Vector2, velocity: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(position))
    world.add_component(sprite_entity, CVelocity(velocity))
    world.add_component(sprite_entity, CSurface.from_surface(surface))

    return sprite_entity


def create_enemy_square(world: esper.World, position: pygame.Vector2, enemy_info: dict):
    enemy_surface = pygame.image.load(enemy_info["image"]).convert_alpha()
    velocity_max = enemy_info["velocity_max"]
    velocity_min = enemy_info["velocity_min"]
    velocity = pygame.Vector2(0, 0)
    while velocity.x == 0 and velocity.y == 0:
        velocity_range = random.randrange(velocity_min, velocity_max)
        velocity = pygame.Vector2(
            random.choice([-velocity_range, velocity_range]),
            random.choice([-velocity_range, velocity_range])
        )

    enemy_entity = create_sprite(world, position, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy())
    return enemy_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(
        level_data['enemy_spawn_events']))


def create_player_square(world: esper.World, player_info: dict, player_level_info: dict) -> int:
    player_sprite = pygame.image.load(player_info["image"]).convert_alpha()
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])
    x, y = tuple(player_level_info["position"].values())
    position = pygame.Vector2(x - (size[0]/2), y - (size[1]/2))
    velocity = pygame.Vector2(0, 0)

    player_entity = create_sprite(world, position, velocity, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_right_mouse = world.create_entity()
    world.add_component(input_left, CInputCommand(
        "PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, CInputCommand(
        "PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down, CInputCommand(
        "PLAYER_DOWN", pygame.K_DOWN))
    world.add_component(input_right_mouse, CInputCommand(
        "PLAYER_FIRE", pygame.BUTTON_RIGHT))


def create_bullet_square(world: esper.World, bullet_info: dict, player_entity: int, mouse_position: pygame.Vector2) -> int:
    bullet_surface = pygame.image.load(
        bullet_info["image"]).convert_alpha()
    player_position = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)
    bullet_size = bullet_surface.get_rect().size
    position = pygame.Vector2(
        player_position.position.x +
        player_surface.area.size[0]/2 - (bullet_size[0]/2),
        player_position.position.y +
        player_surface.area.size[1]/2 - (bullet_size[1]/2)
    )
    direction = (mouse_position - position).normalize()

    velocity = pygame.Vector2(direction.x * bullet_info["velocity"],
                              direction.y * bullet_info["velocity"])

    bullet_entity = create_sprite(
        world, position, velocity, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    return bullet_entity
