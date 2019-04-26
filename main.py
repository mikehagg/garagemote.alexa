from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
# from ask_sdk_model.ui import SimpleCard
from modules.utilities import render_template
from modules.garage_api import get_garage_door_status, get_garage_heat_index, get_garage_humidity, \
     get_garage_temp, set_garage_desired_state


skill_name = "Garage Door"
door_1_name = "large"
door_2_name = "small"

sb = SkillBuilder()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launched(handler_input):
    welcome = render_template('welcome')
    handler_input.response_builder \
        .speak(welcome) \
        .ask(welcome)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Garage_Door_Status_Intent"))
def garage_door_status(handler_input):

    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots

    which_door = str(slots['which_door'].value)

    if which_door == 'None':
        which_door = "both"

    if which_door == "both":
        text = render_template('garage_door_status_both', ld_state=get_garage_door_status(door_1_name),
                               sd_state=get_garage_door_status(door_2_name))
    else:
        text = render_template('garage_door_status_one', which=which_door,
                               state=get_garage_door_status(which_door))
    handler_input.response_builder \
        .speak(text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Garage_Door_Open_Intent"))
def garage_door_open(handler_input):
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots
    session_attributes = handler_input.attributes_manager.session_attributes

    which_door = str(slots['which_door'].value)

    if which_door == 'None':
        which_door = "both"

    if which_door == "both":
        door_1_door_status = get_garage_door_status(door_1_name)
        door_2_door_status = get_garage_door_status(door_2_name)
        if door_1_door_status == "closed":
            set_garage_desired_state(door_1_name, "open")
        if door_2_door_status == "closed":
            set_garage_desired_state(door_2_name, "open")
        text = render_template('garage_door_status_both', ld_state=get_garage_door_status(door_1_name),
                               sd_state=get_garage_door_status(door_2_name))
        handler_input.response_builder.speak(text)
        return handler_input.response_builder.response
    else:
        status = get_garage_door_status(which_door)
        # print(which_door + " door is currently " + status)
        if status == "closed":
            if which_door == door_1_name:
                set_garage_desired_state(door_1_name, "open")
            elif which_door == door_2_name:
                set_garage_desired_state(door_2_name, "open")
            # time.sleep(1)
            text = render_template('garage_door_status_one', which=which_door,
                                   state=get_garage_door_status(which_door))
            handler_input.response_builder.speak(text)
            return handler_input.response_builder.response
        elif status == "unknown":
            text = render_template('garage_door_unknown', which=which_door)
            handler_input.response_builder \
                .speak(text)
            return handler_input.response_builder.response
        else:
            text = render_template('garage_door_open', which=which_door)
            session_attributes["CLOSE_GARAGE_DOOR"] = True
            session_attributes["WHICH_DOOR"] = which_door
            handler_input.response_builder \
                .speak(text) \
                .ask(text)
            return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Garage_Door_Close_Intent"))
def garage_door_close(handler_input):
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots
    session_attributes = handler_input.attributes_manager.session_attributes

    which_door = str(slots['which_door'].value)
    if which_door == 'None':
        which_door = "both"

    if which_door == "both":
        door_1_door_status = get_garage_door_status(door_1_name)
        door_2_door_status = get_garage_door_status(door_2_name)
        if door_1_door_status == "open":
            set_garage_desired_state(door_1_name, "closed")
        if door_2_door_status == "open":
            set_garage_desired_state(door_2_name, "closed")
        text = render_template('garage_door_status_both', ld_state=get_garage_door_status(door_1_name),
                               sd_state=get_garage_door_status(door_2_name))
        handler_input.response_builder.speak(text)
        return handler_input.response_builder.response
    else:
        status = get_garage_door_status(which_door)
        if status == "open":
            if which_door == door_1_name:
                set_garage_desired_state(door_1_name, "closed")
            elif which_door == door_2_name:
                set_garage_desired_state(door_2_name, "closed")
            text = render_template('garage_door_status_one', which=which_door,
                                   state=get_garage_door_status(which_door))
            handler_input.response_builder.speak(text)
            return handler_input.response_builder.response
        elif status == "unknown":
            text = render_template('garage_door_unknown', which=which_door)
            handler_input.response_builder \
                .speak(text) \
                .ask(text)
            return handler_input.response_builder.response
        else:
            text = render_template('garage_door_close', which=which_door)
            session_attributes["OPEN_GARAGE_DOOR"] = True
            session_attributes["WHICH_DOOR"] = which_door
            handler_input.response_builder \
                .speak(text) \
                .ask(text)
            return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Garage_Weather_Intent"))
def garage_weather(handler_input):
    text = render_template('garage_weather', temp=get_garage_temp(),
                           humidity=get_garage_humidity(),
                           heat_index=get_garage_heat_index())
    handler_input.response_builder \
        .speak(text) \
        .ask(text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Yes_Intent"))
def yes_handler(handler_input):
    session_attributes = handler_input.attributes_manager.session_attributes
    if session_attributes.get("CLOSE_GARAGE_DOOR"):
        session_attributes["CLOSE_GARAGE_DOOR"] = False
        return garage_door_close()
    elif session_attributes.get("OPEN_GARAGE_DOOR"):
        session_attributes["OPEN_GARAGE_DOOR"] = False
        return garage_door_open()
    else:
        text = render_template('garage_help')
        handler_input.response_builder \
            .speak(text) \
            .ask(text)
        return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("No_Intent"))
def no_handler(handler_input):
    text = render_template('garage_goodbye')
    handler_input.response_builder \
        .speak(text) \
        .ask(text)
    return handler_input.response_builder.response


# Handler to be provided in lambda console.
lambda_handler = sb.lambda_handler()
