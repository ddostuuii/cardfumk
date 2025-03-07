import subprocess
import time
import os
import psutil

def set_high_priority():
    """ प्रोसेस को हाई प्रायोरिटी देने के लिए यह फंक्शन है। """
    try:
        p = psutil.Process(os.getpid())
        p.nice(psutil.REALTIME_PRIORITY_CLASS)  # Windows के लिए
    except AttributeError:
        os.nice(-20)  # Linux/macOS के लिए (सबसे हाई प्रायोरिटी)

def restart_bot():
    """ हर 30 मिनट में main.py को रीस्टार्ट करेगा। """
    while True:
        print("🔄 Restarting main.py...")
        bot_process = subprocess.Popen(["python", "main.py"])

        # 30 मिनट (1800 सेकंड) तक वेट करो
        time.sleep(1800)

        # बोट को टर्मिनेट करके फिर से स्टार्ट करो
        bot_process.terminate()
        bot_process.wait()

if __name__ == "__main__":
    set_high_priority()  # बोट को हाई प्रायोरिटी देना
    restart_bot()  # बोट को ऑटो-रीस्टार्ट करना
