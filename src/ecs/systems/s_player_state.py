import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity


def system_player_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)

    for _, (c_velocity, c_animation, c_player_state) in components:
        if c_player_state.state == PlayerState.IDLE:
            _do_idle_state(c_velocity, c_animation, c_player_state)
        elif c_player_state.state == PlayerState.MOVE:
            _do_move_state(c_velocity, c_animation, c_player_state)


def _do_idle_state(c_velocity: CVelocity, c_animation: CAnimation, c_player_state: CPlayerState):
    _set_animation(c_animation, 1)

    if c_velocity.velocity.magnitude_squared() > 0:
        c_player_state.state = PlayerState.MOVE


def _do_move_state(c_velocity: CVelocity, c_animation: CAnimation, c_player_state: CPlayerState):
    _set_animation(c_animation, 0)

    if c_velocity.velocity.magnitude_squared() <= 0:
        c_player_state.state = PlayerState.IDLE


def _set_animation(c_animation: CAnimation, animation_number: int):
    if c_animation.current_animation == animation_number:
        return

    c_animation.current_animation = animation_number
    c_animation.current_animation_time = 0

    c_animation.current_frame = c_animation.current_frame = c_animation.animations_list[
        c_animation.current_animation].start
