#!/usr/bin/env python3
import rospy, os, sys, telebot, signal, time
from geometry_msgs.msg import Twist
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
bot = telebot.TeleBot('')#paste here bot token
speed_mult=1 #linear speed multiplier
ang_speed_mult=1 #angular speed multiplier

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

def gen_markup():
    markup = ReplyKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("↪️"),
    InlineKeyboardButton("↩️"))
    markup.add(InlineKeyboardButton("↖️", callback_data="tl"),
    InlineKeyboardButton("⬆️", callback_data="tt"),
    InlineKeyboardButton("↗️", callback_data="tr"),row_width=3)
    markup.add(InlineKeyboardButton("⬅️", callback_data="cl"),
    InlineKeyboardButton("⏹", callback_data="cc"),
    InlineKeyboardButton("➡️", callback_data="cr"))
    markup.add(InlineKeyboardButton("↙️", callback_data="bl"),
    InlineKeyboardButton("⬇️", callback_data="bb"),
    InlineKeyboardButton("↘️", callback_data="br"))
    return markup

def gen_markup2():
    markup = ReplyKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("speed-10%"),
    InlineKeyboardButton("⏺"),
    InlineKeyboardButton("speed+10%"))
    markup.add(InlineKeyboardButton("ang speed-10%"),
    InlineKeyboardButton("ang speed+10%"))
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'I am remote controller for robotont. Welcome {message.from_user.first_name}! \nCommand for keyboard is /keyboard')

def timer_callback(event):
	global last_heartbeat
	if (rospy.get_time() - last_heartbeat) >= 0.5:
		cmd_vel_pub.publish(Twist())

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    twist_msg = Twist()
    global ang_speed_mult, speed_mult, last_heartbeat
    last_heartbeat = rospy.get_time()
    if message.text.lower() == '/keyboard' or message.text == '⏺':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Robot control", reply_markup=gen_markup())
    elif message.text == '↖️':
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.x=1*speed_mult
        twist_msg.linear.y=1*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "⬆️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.x=1*speed_mult
        twist_msg.linear.y=0*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "↗️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.x=0.3*speed_mult
        twist_msg.linear.y=-0.3*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "⬅️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=0.3*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "⏹": 
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Adjust speeds", reply_markup=gen_markup2())
        twist_msg.linear.y=0.3*speed_mult
        twist_msg.linear.x=0.3*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "➡️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=-0.3*speed_mult
        twist_msg.linear.x=0*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "↙️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=0.3*speed_mult
        twist_msg.linear.x=-0.3*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "⬇️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=0*speed_mult
        twist_msg.linear.x=-0.3*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "↘️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=-0.3*speed_mult
        twist_msg.linear.x=-0.3*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "↪️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.angular.z=0.79*ang_speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "↩️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.angular.z=-0.79*ang_speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "ang speed+10%":
        bot.delete_message(message.chat.id, message.message_id)
        ang_speed_mult= ang_speed_mult*1.1 if ang_speed_mult*1.1<1 else 1
        bot.send_message(message.chat.id, f"Ang speed: {ang_speed_mult}")
    elif message.text == "ang speed-10%":
        bot.delete_message(message.chat.id, message.message_id)
        ang_speed_mult*=0.9
    elif message.text == "speed+10%":
        bot.delete_message(message.chat.id, message.message_id)
        speed_mult= speed_mult*1.1 if speed_mult*1.1<0.35 else 0.35
        bot.send_message(message.chat.id, f"Linear speed: {speed_mult}")
    elif message.text == "speed-10%":
        bot.delete_message(message.chat.id, message.message_id)
        speed_mult*=0.9
        bot.send_message(message.chat.id, f"Linear speed: {speed_mult}")
    else:
        bot.send_message(message.from_user.id, 'Command not recognized')
        sleep(2)

def signal_handler():
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler) # To help bot die 
    rospy.init_node('telegram_bot', anonymous = True)
    global cmd_vel_pub
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    global last_heartbeat
    last_heartbeat = rospy.get_time()
    t = rospy.Timer(rospy.Duration(0.5), timer_callback)
    rospy.sleep(1)

    bot.polling()

