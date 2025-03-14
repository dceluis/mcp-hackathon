piano tutor?

kid todo app

deals monitored by an agent using mcp

auto llms.txt

auto end-to-end testing applications through mcp

a text based game of any sorts that battles llms through some sort of
intelligence battle.

an app that gives (ai) instructions to grandpas about how to do important things on
their phones.

driving test simulator with ai generated test scenarios

!tasker mcp server

why?

tasker is an automation tool for Android. It allows you to call phone actions
like get contacts, interact with the screen, read screen contents and so on.

It is very powerful as in it allow you to basically create applications without
having to write an apk for it.

The problem is that creating 'tasks' in tasker is time consuming because its
done through a phone ui. And 'programming' the task as code is not a easy fit
eitebr because it uses a custom xml format that is very hard to work with.

So, my idea is to create a big tasker project that provides atomic tasks for
most of the existing tasker actions and provide an mcp server so that llms can
create applications on the fly with just the action definitions. without needing
to manually create tasks using the tasker ui.

I a sense, tasker is an api for android automation

Writing an application for phone automation in:

lang,                 power,          simplicity
Kotlin or Java,       highest,        lowest
tasker,               high,           medium *
tasker mcp,           medium**,       easy***

*graphical ui is time consuming
** it will never be possible to implement the full feature set of tasker on the mcp server (unless we provide some meta action that can create actions in tasker??, out of scope in this hackathon version)
*** text based instructions. even better, voice instructions***

I think that if implemented correctly it will be a sort of open source google
assistant. And even better, because google assistant has only a small number of
things it can outomate (mostly google services), whereas with tasker, your
imagination is the limit

---
02-28 @ 21:16

Ok, i read about the mcp specification and it seems to encompass a communication
protocol, a server specification, and client specifications.

for this project the server can be a project that implements all the atomic
tasks, and a simple http server can be also made with tasker.

now the question is how do we implement the client and host. i see two options.

1. create a simple application in kotlin to run a simple agentic loop and use
the kotlin sdk to implement a client that will call the tasker server.
the pros is that theres already a kotlin sdk and if the http server is setup
correctly it should work out of the box? the con is that i need to setup and
build an android app! probably not too bad though claude should help me with
this but i'd still spend time learning android app development

2. create a tasker ui for the agentic loop and interact with the server.
would need to make sure that the client project and the server projects are
completely separate. pro is that its just a tasker project that others can
import, cons creating a complex tasker project is no easy task and i think this
would take at least the same amount of time as building the server project.

3. if all goes sour and i only have time to create the server project i think
the worst option is not implementing any client and leaving it at that
meaning the client is left for users to implement.
I dont think a submission without any functioning demo is going to win any
prizes though :(


---
02-28 @ 21:24

ooookk, so to implement a proper mcp server there is also sdks involves its not
just a matter of conforming to a response schema sooo this might be harder than
i thought. still there's always termux which can call tasker tasks i think? 

---
02-28 @ 21:37

so gemini 2 talked me out of implementing the server in tasker lol. its too
complex and most probably impossible because tasker does not have enough tools
to maintain state, persistent connections, two way communication, its too slow
etc etc.

we need a bridge that can still call tasker functions and read the tasker responses. and
communicate with the clients. i am going to try termux with the python mcp
library if this does not work then id say i need to pivot to another submission

---
02-28 @ 22:14

so i setup the termux env and sshd to it. testing the server

---
02-28 @ 23:57

installing termux dependencies and getting the whole thing to run is a nightmare
i had to install rust and python and pip is still installing the depenndencies
but i still have hope

---
03-01 @ 01:25

so at last i could create a server that runs on termux and a sample client that
i can call from my pc that will connect to termux and run a tool. right now its
just printing a toast but itss something!

---
03-01 @ 02:10

I found [this](https://www.reddit.com/r/tasker/comments/17ygxvq/is_there_a_way_you_call_a_tasker_task_from_termux/) page that says how to run 
tasker task from termux. thats exactly what i needed

although it just sends the activity i still need to handle the response
i created termux-tasker script to install to termux

---
03-01 @ 06:18

I added a chat loop with Gemini 2.0 flash and tool calling.

---
03-01 @ 14:26

I have been investigating better ways of calling tasks than the am method.

The problem with sending an intent is that its a send and forget method. We
would need to implement a callback listener in the mcp server get return the
task response back. And also we would need to implement unique task run ids and
so on.

Instead, you can create a tasker http web server with an endpoint that will
run  a task and return with the response. I will be implementing it this way.

---
03-01 @ 14:55

[Tasker RCE](https://www.reddit.com/r/tasker/comments/1isg6ve/dev_tasker_6413_widget_v2_remote_action_execution/)

SoOOO very interestingly, seems like tasker just recently added a remote action
execution feature. It it provides an http endpoint that you need to authenticate with a firebase acct and
a device secret token?

Its nice but still thats probably too much setup for remote access when i only
need accessing it from the server that will live on the device for now. I may
implement my own version of tbis later. Also, running in the same wifi network
I can access the mcp server on my device just fine, pointing to the device ip

plus, i looked at the demo and i did not see any response collection so it
seems that it would also fire and forget a task. So i would still need to
include a callback mechanism anyways. hmmm it doesnt sound like a bad idea but i
will stick to my plan for now.

---
03-01 @ 15:09

wait, some user in teb hackathon chat posted that they added their tools to their custom gpt?
this would simplify the development so much

are there any ai other clients that integrate with mcp servers???

---
03-01 @ 19:14

I cant believe how long it took me to setup LibreChat but the good news is that the mcp
server is working good!! I can interact with it through any model and it just works.

![image](https://github.com/user-attachments/assets/77a8ef01-0321-49c1-8b26-1d93224a7166)

Now what I will spend the rest of the day adding as many tasks as I can to the tasker mcp project,
most importantly making the screenshot tool work.

---
03-02 @ 00:05

So, I investigated how to render or work with images as results of tool calls. AFAIK 
this is not supported by clients like libreChat and others.

So probably if i want to do this i need to use smolagents or cook up my own
image-aware ReAct loop. Probably package this on a simple web server too so
that i can access it from my phone through local LAN for demo purposes.

I should probably start recording and editing the small use cases demo.

Ideally i want to record 3 demos. one for simple tasks like clipboard, info,
alarms, etc. aNother one for medium more interesting tasks or combination of
tasks like playing songs or whatever i come up with later. and finally the demo
that would be awesome to have is a visual, multi step navigation demo which i
need image observation for. So, I have 2 demos to record and hopefully i still
have time to tackle the ReAct app with images.

---
03-02 @ 11:03

So yesterday was an ok day for brainstorming but i did not really get much done
in terms of coding. I created a small draft of myy presentation but i should
come up with more compelling demo cases and a shorter presentation.

---
03-02 @ 19:38

Running out of time but i have a good draft of the demo i want to make. I will
present a comparison video showing gemini assistant and this assistant. Showing
that its just as good an even better. I Just got the print task working and I
think it will make for a great show..

---
03-02 @ 20:31

I think I have enough actions for a good demo. I will start recording them and
finishing the script
