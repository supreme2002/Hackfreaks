#Written by @Surv_ivor, Further Edited by @TheFSociety2_0

import html
from telegram import Message, Update, Bot, User, Chat, ParseMode
from typing import List, Optional
from telegram.error import BadRequest, TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html
from SaitamaRobot import dispatcher, OWNER_ID, DRAGONS, DEMONS, EVENT_LOGS, DEV_USERS
from SaitamaRobot.modules.helper_funcs.chat_status import user_admin, is_user_admin
from SaitamaRobot.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from SaitamaRobot.modules.helper_funcs.filters import CustomFilters
from SaitamaRobot.modules.helper_funcs.misc import send_to_list
from SaitamaRobot.modules.sql.users_sql import get_all_chats
import SaitamaRobot.modules.sql.global_kicks_sql as sql

GKICK_ERRORS = {
    "Bots can't add new chat members",
    "Channel_private",
    "Chat not found",
    "Can't demote chat creator",
    "Chat_admin_required",
    "Group chat was deactivated",
    "Method is available for supergroup and channel chats only",
    "Method is available only for supergroups",
    "Need to be inviter of a user to kick it from a basic group",
    "Not enough rights to restrict/unrestrict chat member",
    "Not in the chat",
    "Only the creator of a basic group can kick group administrators",
    "Peer_id_invalid",
    "User is an administrator of the chat",
    "User_not_participant",
    "Reply message not found",
    "Can't remove chat owner",
    "User not found"
}

@run_async
def gkick(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id = extract_user(message, args)
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in GKICK_ERRORS:
            pass
        else:
            message.reply_text("User cannot be Globally kicked because: {}".format(excp.message))
            return
    except TelegramError:
            pass

    if not user_id or int(user_id)==777000:
        message.reply_text("You don't seem to be referring to a user.")
        return
    if int(user_id) in DRAGONS or int(user_id) in DEMONS or int(user_id) in DEV_USERS:
        message.reply_text("OHHH! Someone's trying to gkick an Elite/Knightmen user! *Grabs popcorn*")
        return
    if int(user_id) == OWNER_ID:
        message.reply_text("Wow! Someone's so noob that he want to gkick the Emperor! *Grabs Potato Chips*")
        return

    if user_id == 1228116248:
        message.reply_text("There is no way I can gkick this user.He is my Creator/Developer")
        return

    if user_id == bot.id:
        message.reply_text("Welp, I'm not gonna to gkick myself!")
        return    

    chats = get_all_chats()
    banner = update.effective_user  # type: Optional[User]
    log_message = (
                 "<b>Global Kick</b>" \
                 "\n#GKICK" \
                 "\n<b>Status:</b> <code>Enforcing</code>" \
                 "\n<b>Sudo Admin:</b> {}" \
                 "\n<b>User:</b> {}" \
                 "\n<b>ID:</b> <code>{}</code>".format(mention_html(banner.id, banner.first_name),
                                              mention_html(user_chat.id, user_chat.first_name), 
                                                           user_chat.id))
    if EVENT_LOGS:
        try:
            log = bot.send_message(
                EVENT_LOGS, log_message, parse_mode=ParseMode.HTML)
        except BadRequest as e:
            print(e)
            log = bot.send_message(
                EVENT_LOGS,
                log_message +
                "\n\nFormatting has been disabled due to an unexpected error.")

    else:
        send_to_list(bot, DRAGONS + DEV_USERS, log_message, html=True)
	
    message.reply_text("Globally kicking user {}".format(user_chat.first_name))
    sql.gkick_user(user_id, user_chat.username, 1)
    for chat in chats:
        try:
            member = bot.get_chat_member(chat.chat_id, user_id)
            if member.can_send_messages is False:
                bot.unban_chat_member(chat.chat_id, user_id)  # Unban_member = kick (and not ban)
                bot.restrict_chat_member(chat.chat_id, user_id, can_send_messages = False)
            else:
                bot.unban_chat_member(chat.chat_id, user_id)
        except BadRequest as excp:
            if excp.message in GKICK_ERRORS:
                pass
            else:
                message.reply_text("User cannot be Globally kicked because: {}".format(excp.message))
                return
        except TelegramError:
            pass

def __user_info__(user_id):
    times = sql.get_times(user_id)
    
    if int(user_id) in DRAGONS or int(user_id) in DEMONS:
        text="Globally kicked: <b>No</b> (Immortal)"
    else:
        text = "Globally kicked: {}"
        if times!=0:
            text = text.format("<b>Yes</b> (Times: {})".format(times))
        else:
            text = text.format("<b>No</b>")
    return text

@run_async
def gkickset(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id, value = extract_user_and_text(message, args)
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in GKICK_ERRORS:
            pass
        else:
            message.reply_text("GENERIC ERROR: {}".format(excp.message))
    except TelegramError:
        pass
    if not user_id:
        message.reply_text("You do not seems to be referring to a user")
        return  
    if int(user_id) in DRAGONS or int(user_id) in DEMONS:
        message.reply_text("ELITE: Irrelevant")
        return
    if int(user_id) == OWNER_ID:
        message.reply_text("EMPEROR: Irrelevant")
        return
    if user_id == bot.id:
        message.reply_text("It's me, nigga")
        return
      
    sql.gkick_setvalue(user_id, user_chat.username, int(value))
    return

def gkickreset(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id, value = extract_user_and_text(message, args)
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in GKICK_ERRORS:
            pass
        else:
            message.reply_text("GENERIC ERROR: {}".format(excp.message))
    except TelegramError:
        pass
    if not user_id:
        message.reply_text("You do not seems to be referring to a user")
        return  
    if int(user_id) in DRAGONS or int(user_id) in DEMONS:
        message.reply_text("ELITE: Irrelevant")
        return
    if int(user_id) == OWNER_ID:
        message.reply_text("EMPEROR: Irrelevant")
        return
    if user_id == bot.id:
        message.reply_text("It's me, nigga")
        return
      
    sql.gkick_reset(user_id)
    return

__help__ = """
*Admin only:*
- /gkick: To kick a user Globaly
- /gkickset: Set global kick status of a person
- /gkickreser: Reset global kick status of a person
"""

__mod_name__ = "GLOBAL KICK"
			
GKICK_HANDLER = CommandHandler("gkick", gkick, pass_args=True,
                              filters=CustomFilters.sudo_filter | CustomFilters.support_filter)
SET_HANDLER = CommandHandler("gkickset", gkickset, pass_args=True,filters=Filters.user(OWNER_ID))
RESET_HANDLER = CommandHandler("gkickreset", gkickreset, pass_args=True,filters=Filters.user(OWNER_ID))

dispatcher.add_handler(GKICK_HANDLER)
dispatcher.add_handler(SET_HANDLER)
dispatcher.add_handler(RESET_HANDLER)
