# PyNotifyYou

A simple library for sending notifications

**Attention**! I'm **far from the most experienced or smart developer**, so I'm **not denying** that my  code can be pretty bad! I will **always** be glad to receive your **advice on improving the code** and **ideas** for implementation.

I also want to say that this is my first library, and most likely I will use quite a lot of old and crooked nonsense. Please don't blame me for this 👻

# Navigation

Let's add some convenience for navigating through the repository:

 - [☁️Welcome☁️](#PyNotifyYou)
 - [🧭Navigation🧭](#Navigation)
 - [🐍 Providers 🐍](#Providers)
 - [🔨Installing🔨](#Installing)
 - [✅Usage✅](#PyNotifyYou)


# Providers
I plan to implement support for several ways to receive notifications, and I will simply call them providers for convenience. 👌

**At the moment**, the project supports only one provider: **Ntfy.sh**

# Installing

Okay, let's move on to the installation! In fact, the installation is no different from other libraries

You just need to install the library via pip:
```shell
pip install py_notify_you
```


# Usage

And here it 's more interesting!

You can see the simplest option for sending notifications below.

Since the example uses Ntfy you need to perform the following steps:

To receive notifications, you must install the Ntfy app on your phone([Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy),[IOS](https://apps.apple.com/us/app/ntfy/id1625396347)) or install [PWA](https://docs.ntfy.sh/subscribe/pwa/)!

Then click on the "+" button in the lower right corner to create a topic and get link (It will be needed in the future)

When creating, you will be required to enter the name of the topic, which will be a link, for example:
- The link Topic with the name PyNotifyMe will look like this - https://ntfy.sh/PyNotifyMe
- The link Topic with the name PythonStore will look like this - https://ntfy.sh/PythonStore

***

Now all that remains is to write the code! For the easiest way to send notifications, you can use the code below:
```python
import py_notify_you

sender = py_notify_you.Ntfy("https://ntfy.sh/YourLink") #  Here you should replace the link with your own
sender.send('Your message!')
```
**DON'T FORGET TO CHANGE THE LINK**


You can also add a header for your notification using the method ```set_title()``` :

```python
import PyNotifyYou

sender = py_notify_you.Ntfy("https://ntfy.sh/YourLink") #  Here you should replace the link with your own
sender.set_title("Your title")
sender.send('Your message!')
```

<<<<<<< HEAD
More information can be found on the project's [wiki](https://github.com/shizamuru-dev/PyNotifyYou/wiki)
=======
More information can be found on the project's [wiki](https://github.com/shizamuru-dev/PyNotifyYou/wiki)
>>>>>>> 83c61adefea64f07b2cfdaddc69b12298ccaeb79
