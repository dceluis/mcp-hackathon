Tasks ![](icon_tasker.png)
--------------------------

A task is simply a set of actions which are performed one after the other.

#### Named / Anonymous Tasks

A task can be given a name. This allows:

*   the same task to be used in more than one profile
*   easier identification of what the task does*   in the case of a task widget/shortcut, it provides a label for the icon on the home screen.

When creating a profile, widget or shortcut, often the associated task will consist only of one or two actions which will not be reused. For this case, Tasker allows you to create a task without a name (an _Anonymous_ task).

#### Task Scheduling

When there is a single task waiting to be executed, it's actions are executed one-by-one until finished.

When there are several tasks in the queue at once, it's important to understand how they are handled:

*   only **one action** from the same [action group](#actiongroups) can be executed at once to prevent interference
*   the task in the queue with the **highest priority** goes first and blocks lower priority tasks
*   tasks with the **same priority** take turns executing an action each, starting with the most recent addition to the queue **unless** one task is a child of the other (started via [Perform Task](#help/ah_run_task.html)), in which case the child executes first.

Task priority, 0 to 50 inclusive with 0 being lowest, is determined according to whatever causes the task to run.

*   enter tasks run by profiles have the priority specified in Profile Properties, the default is 5.
*   exit tasks run by profiles have the priority specified in Profile Properties **plus 1001**, the default is therefore 1016
*   tasks run by **widgets** or **shortcuts** can be set in Task Properties when the widget/shortcut is created, the default is 7
*   tasks run from scene elements have priority **one more** than the task which showed the scene
*   tasks run from the **Test** button in the task edit screen have priority 100 by default, long-click the play buttin to choose a different one.

A couple of guidelines are:

*   if you want a particular task to always interrupt other tasks that may be executing, give it a high priority
*   if you have a task that lasts for a while, you probably want to give it a low priority so it doesn't block other tasks from being executed.

#### Action Groups

Actions are divided into groups for scheduling based on how long the action takes to execute and what it interferes with:

*   **Speech**: `Say, Say To File`
*   **Javascript**: `Javascript`
*   **Fix**: `Get Location`
*   **Voice**: `Get Voice`
*   **Proxy**: `Display Brightness, Query Action, Photo, Photo Series, Photo Series Time`
*   **Proxy Scene** Enter Key, Menu, Popup, Popup Task Buttons, Variable Query
*   **Other Scenes**: the name of the scene being shown
*   **Normal**: all other actions

#### Wait Actions

`Wait` and `Wait Until` are special cases. The rules for handling them are complicated and try to do the 'best thing' dependent on the situation.

#### Same-Profile Tasks

Tasks launched by the same profile by default always execute in the order in which they are launched. Other tasks from the same profile remain completely inactive until any previous task from the same profile is complete. The main purpose of this rule is to correctly handle rapid changes in a profile's activation state.

This behaviour can be disabled by deselecting _Enforce Task Order_ in the Profile Properties dialog.

##### Example

This example demonstrates the effect of Enforce Task Order and shows also how sub-tasks launched by [Perform Task](#help/ah_run_task.html) are handled.

Profile: Example
Enter Task: Enter1
   Perform Task, Enter2
Exit Task: Exit1
   Perform Task, Exit2

**With** Enforce Task Order:

Enter1 and Enter2 are both guaranteed to finish before either of Exit1 or Exit2. Whether Enter1 or Enter2 finishes first depends on their relative priority. Same for Exit1 and Exit2. All 4 tasks compete based on priority against tasks from other profiles. Exit tasks have a higher base priority so will finish before Enter tasks.

**Without** Enforce Task Order:

If the profile goes active and inactive quickly, Enter1, Enter2, Exit1 and Exit2 will all compete purely on priority. Since Exit tasks have higher base priority, Exit1 and Exit2 will probably finish first.

#### Collisions

Sometimes a task needs to be executed of which a copy is already executing. This can happen quite often e.g. when a task widget button is pressed twice quickly, or a task contains a Wait action or shows a dialog.

The way in which a collision is resolved is specified by the user. There are 3 options:

*   the **new** task is ignored (the default)
*   the **existing** task is aborted and the new one starts from its first action. The current action of the previous task is finished if it is already being carried out.
*   both tasks run simultaneously

Note that the last option can lead to several copies of a task all running at once.

#### Behaviour When Device Off

By default, after a few seconds of the screen being off Android will power down the device and thus running tasks will be paused.

In the Task Properties dialog, it can be specified that a task should keep running.

##### Dialogs

An action that shows some kind of dialog (such as a lock screen, popup, menu) blocks execution of any other action, even one of higher priority, until it is completed.

##### Wait / Wait Until

These are exceptions. A wait action can be interrupted by another task's action and will resume (if necessary) when the other task's action is finished.

#### Killing Tasks

If you have a problem with a task that never ends, you can manually end tasks with the **Kill** button in the Task Edit screen.

Flow Control ![](icon_tasker.png) 
----------------------------------

#### Overview

Task flow control is based on the following Tasker elements:

*   [variable](#variables.html) values
*   [conditions](#condition) on individual actions
*   _If / Else / Endif_ actions for conditional grouping of following actions
*   _For / End For_ to do a set of actions once for each of a set of elements
*   _Goto_ action (jumping around within a task).
*   _Perform Task_ action (calling other tasks as subroutines)
*   _Stop_ action (terminate task immediately)

On the Wiki there is a detailed example of [processing a file's content](http://tasker.wikidot.com/fileproc) \[External Link\].

Tip: if you accidentally create a task that never ends when experimenting with loops, use the **Kill** button in the Task Edit screen to end it manually.

##### Conditions

Every action can have a condition associated with it (specify this in the Action Edit screen). If the condition does not match, the action will be skipped.

A condition consists of an _operator_ ('equals' etc) and two _parameters_. The possible operators are:

*   _Equals_ (eq)  
    The left parameter is identical to the right parameter.
*   _Doesn't Equal_ (neq)  
    The left parameter is not identical to the right parameter.*   _Matches_ (~)  
    The right parameter is a pattern which the left parameter is [matched against](#matching.html).
*   _Not Matches_ (!~)  
    As above, but the match must fail for the action to be executed.
*   _Matches Regex_ (~R)  
    The right parameter is a regular expression which the left parameter is [matched against](#regex).
*   _Doesn't Match Regex_ (!~R)  
    As above, but the match must fail for the action to be executed.
*   _Maths: Less Than_ (<)  
    Both parameters (after variables are substitued) must be numbers or mathematical expressions and the first must be **less** than the second e.g. `3` < `6`. See [Maths](#maths.html) for more info.
*   _Maths: Greater Than_ (>)  
    As above, but the first parameter must evaluate to **more** than the second.
*   _Maths: Equals_ (=)  
    As above, but the two parameters must be numerically equal.
*   _Maths: Isn't Equal To_ (!=)  
    As above, but the two parameters must be **not** numerically equal.
*   _Maths: Is Even_ (Even)  
    The left parameter is an even number.
*   _Maths: Is Odd_ (Odd)  
    The left parameter is an odd number.
*   _Is/Isn't Set_ (Set/!Set)  
    Whether the specified variable has a value or not.

Expressions which are not mathematically valid e.g. _I Am The Walrus > 5_ give a warning and evaluate to **false** when used with a mathematical operator.

#### Foreach Loop

Goal: perform a set of actions for each of _apple_, _pear_ and _banana_.

| Id | Action                                                                  | Desc                                                   |
| -- | ----------------------------------------------------------------------- | ------------------------------------------------------ |
| 1. | **For**<br>%item<br>apple,pear,banana                                   | Loop once for each of apple, pear and banana           |
| 2. | **Action One**                                                          | Example: Flash %item                                   |
| 3. | **Action Two**                                                          | ...                                                    |
| 4. | **End For**                                                             | Return to action 1 if we havn't done all the items yet |

Result: Action One and Action Two are performed three times. The first time, the variable %item is set to _apple_, the second time _pear_ and the last time _banana_.

You can insert a `Goto` action in the loop with either _Top of Loop_ (meaning continue, skip to the next item straight away) or _End of Loop_ (meaning break, stop without doing any more items) specified.

In adition to simple text, the `For` action accepts any comma-separated combination of these Items:

*   a numeric range e.g. 1:5 (= **1,2,3,4,5**)
*   a numeric range with a jump e.g. 8:2:-2 (= **8,6,4,2**)
*   a numeric range defined by variable values e.g. _2:%end:%skip_, _1:%arr(#)_
*   a variable name (which is replaced) e.g. %fruit (= **banana** maybe)*   a [variable array](#arrays) part e.g. _%arr(1:2)_ (= %arr1, %arr2 = **apple,banana** maybe)

A common case is to use %arr(), which performs a loop for each element in the array %arr.

**Warning**: the _Values_ parameter in the loop is reevaluated with each iteration of the loop, meaning that modifying array variables which appear there from within the loop can have unexpected effects. To workaround that, it can be best to use the following sequence:

       Variables Set, %values, %arrayWhichWillChange()
       Variable Split, %values
       For, %value, %values()
          ...
    

#### For Loop

Goal: perform a set of actions for each of a set of elements in turn.

Use the _Foreach Loop_ as described above, with the _Items_ parameter being a range specification e.g. 4:0, 100, 0:8:2 (= **4,3,2,1,0,100,0,2,4,6,8**).

#### Until Loop

Goal: perform a Task X until some condition is met (at least once)

| Id | Action                                  | Desc                               |
| -- | --------------------------------------- | ---------------------------------- |
| 1. | **Action One**                          | ...                                |
| 2. | **Action Two**                          | ...                                |
| 3. | **Goto**<br>1<br>_If %qtime **<** 20_   | Return to action 1 if runtime < 20 |

Result: Action One and Action Two are performed until %QTIME contains the value 20 or more i.e. until the task has been running for 20 seconds.

Note: %QTIME is a builtin local variable available in all tasks.

#### While Loop

Goal: perform a Task X while some condition is met.

| Id | Action                                        | Desc                                                     |
| -- | --------------------------------------------- | -------------------------------------------------------- |
| 1. | **Stop**<br>_If %fruit **Not Matches** Apple_ | Stop task if it's not Apple, otherwise go to next action |
| 2. | **Action One**                                | ...                                                      |
| 3. | **Action Two**                                | ...                                                      |
| 4. | **Goto**<br>1                                 | Go back and check condition again                        |

Result: Action One and Action Two are performed while %fruit contains the value Apple.

#### Counter Loop

Goal: perform a Task X a set number of times.

| Id | Action                                          | Desc                               |
| -- | ----------------------------------------------- | ---------------------------------- |
| 1. | **Variable Set**<br>%count, 0                   | Initialize the counter             |
| 2. | **Action One**<br>Label: _LoopStart_            | ...                                |
| 3. | **Action Two**                                  | ...                                |
| 4. | **Variable Add**<br>%count, 1                   | Add one to %count                  |
| 5. | **Goto**<br>_LoopStart_<br>_If %count **<** 10_ | Return to action 2 if count < 10   |

Result: after initialization of %count to 0, the task loops around the actions from 2-5 until %count reaches 10, at which point the condition on the `Goto` fails and the end of the task is reached.

Note that we used a `Goto` to a **labelled** action this time. In all but the very simplest tasks it's better to use a label rather than a number. It's easier to work out what's happening and if you insert or delete actions before the loop starts, the `Goto` will still jump to the right place.

An alternative way to do this loop is to use a For action specified as _0:10_.

#### If / Then / Else Condition

Goal: perform certain Tasks if conditions are met, otherwise perform a different task.

| Id | Action                                               | Desc                               |
| -- | ---------------------------------------------------- | ---------------------------------- |
| 1. | **If**<br> _%fruit **~** Apple_                      | **~** is short for 'matches'       |
| 2. | **Action One**                                       | ...                                |
| 3. | **Action Two**                                       | ...                                |
| 4. | **Else If**<br> _%fruit **~** Pear_                  | an `Else` action with a condition  |
| 5. | **Action Three**                                     | ...                                |
| 6. | **Else**                                             |                                    |
| 7. | **Action Four**                                      | ...                                |

Result: actions One and Two are executed if %fruit matches Apple, Action Three is executed if %fruit matches Pear, otherwise Action Four is executed.

Notes:

*   you can have as many `Else If`s in a condition as you like
*   if your condition is in the middle of a more complicated task, you need to tell Tasker where the condition ends with an `End If` action

#### Subroutines

To call another task, use the `Perform Task` action. To use it as a subroutine, you just need to ensure that the priority of the calling task is less than the priority of the called task (more info: [scheduling](#scheduling)).

The parent can optionally pass values to the child and receive a result back:

_Parent Task_

1.

  **Perform Task**  
Child,  
Priority, 10  
%par1, 5,  
Result Value Variable, %result

pass 5 to the child, expect a result in %result

2.

  **Variable Flash**  
Result: %result

what did we get back ?

_Child Task_

1.

  **Variable Set**  
%newval, %par1 + 1, Do Maths

add one to the value that was passed

1.

  **Return**  
%newval  

set %result in the parent to the value of %newval in the child

Result: the parent flashes **6**

Notes:

*   changes made to _%par1_ and _%par2_ in the child task are **not** reflected by their changing in the parent task
*   receiving a return value is optional for the parent, even if the child tries to give it one
*   unlike `Return` statements in most computer languages, Tasker's does not necessarily stop the child task, so if the child and parent have the same priority they can both run together and the child return several results over time.


Icons ![](icon_tasker.png)
--------------------------

Tasker can use four categories of icons: [Application](#app), [Built-In](#builtin), [Ipack](#ipack), [User-Installed](#user).

In some places it's also possible to use any image stored on local media as an icon.

#### Application Icons

These are taken from applications installed on the device.

Minor note: if the icon of the application changes, an update of previously created widgets/shortcuts can be forced by creating a single widget with the new icon and then rebooting.

#### Built-In Icons

These come with Tasker and are kept in the device's memory.

#### Ipack Icon Sets

[Ipack](http://ipack.dinglisch.net) is a free, open format for sharing of icon sets between Android applications. Ipack icon sets can be either installed from [Play Store](http://market.android.com/search?q=ipack) or from the [Ipack website](http://ipack.dinglisch.net/download.html).

When setting an icon, you will notice an item labelled _Download More Icons_. Clicking on it will use the appropriate source depending on which version of Tasker you have.

#### User-Installed Icons

You can also install your own icons directly into Tasker's icon directory `/sdcard/Tasker/.icn/`. Make sure the icons are in a subdirectory. The subdirectory should also only be one level deep (no subsubdirectories).

Icons must be in PNG format.

Example: a two-icon set called _Christmas_ would have the two files in these locations:

> `/sdcard/Tasker/.icn/Christmas/santa.png`  
> `/sdcard/Tasker/.icn/Christmas/snowman.png`

Intents ![](icon_tasker.png)
----------------------------

Intents are Android's main method for allowing apps to communicate with each other and share data. Intents are for advanced users. This document is not intended to explain how intents work, but how to use Tasker's intent facilities.

### Sending Intents

You can find information about intents and details of several built-in Android intents on the Android SDK [Reference Site](# https://developer.android.com/reference/android/content/Intent.html).

Tasker allows you to send arbitraty intents using the _Send Intent_ action in the _Misc_ category. This allows you to provoke behaviour in other apps, when you know the particular form of intent they are designed to respond to.

#### Send Intent Parameters

Note that any parameter specified except Extras will reduce the set of possible receivers of the intent.

##### Action

What the sender would like the receiver to do with the data.

Example: `android.intent.action.VIEW`

##### Cat

Gives additional information about the action.

##### Mime-Type

From the developer reference: "This is used to create intents that only specify a type and not data, for example to indicate the type of data to return."

Can't be used together with a Data specification.

##### Data

The main data specification in the form of a URI.

Can't be used together with a Mime-Type specification.

##### Extras

Any additional data to send with the intent.

The extras must be in the form of a single **colon-separated** key and value.

If the value can be parsed as an integer, long (integer ending in L), floating point number, double (float ending in D) or boolean (true/false) it will be treated as one.

The value can also be forced to a simple type (long etc) or `Uri` via casting.

The name of a Java object created via the Java Function action which is of type `Parcelable` can also be used (e.g. a `Bundle`)

If none of the above apply, the value will be treated as a `String`.

Examples:

*   have\_flowers:true  
    (`boolean`)
*   this.is.an.integer.example:34  
    (`int`)
*   this.is.a.double.example:34D  
    (`int`)
*   address: (Uri) http://a.b  
    (`Uri`)
*   bunchofvalues:mybundle (where mybundle is the name of a Java object of type Bundle)  
    (`Parcelable`)
*   simple.string.example:hello there!  
    (`String`)

##### Package, Class

Allow specification of a particular package and/or class within the package to restrict the broadcast to.

##### Target

The type of Android component which should receive the intent.

#### Finding App Intents

Many intents that an app listens for are declared in its package manifest (called AndroidManifest.xml). You can view details of those intents using the _aapt_ tool that comes with the Android SDK like this:

> `aapt dump xmltree example.apk AndroidManifest.xml`

Look for Intent Filter elements.

It's not (easily) possible to determine which intents an app listens for dynamically (i.e. while the app is running).

### Receiving Intents

Tasker allows you to receive a large range of intents, sent by apps or the system, using the _Intent Received_ event in the _System_ category.

For each event you create, Tasker sets up a corresponding [Intent Filter](https://developer.android.com/reference/android/content/IntentFilter.html) object.

#### Limitations

*   Tasker can only receive intents which are sent to **broadcast receiver** components, not to activities or services.
*   some intent senders require that a corresponding intent filter is specified statically (i.e. in an Android Manifest). Those intents cannot be received.
*   intents which are broadcast with a specification of a particular package component to receive it cannot be received.

#### Send Intent Parameters

##### Action

If specified, the received intent must have also that action specified.

##### Cat

Any categories specified in the received intent must also be specified in the Tasker event. Note that this is logically different to the situation for the Action parameter.

##### Scheme

If any schemes are included in the filter, then an Intent's data must be either one of these schemes or a matching data type. If no schemes are included, then an Intent will match only if it includes no data.

##### Mime Type

If a type is specified, then an Intent's data must be the same, or match the Scheme parameter. If no Mime Type is specified, then an Intent will only match if it specifies no Data.

##### Priority

If the intent is part of an _ordered broadcast_, then the priority specified here will affect whether this event will receive the intent before or after other listeners.

##### Stop Event

If the intent is part of an _ordered broadcast_, then specifying Stop Event will prevent it being passed to other listeners after this one.

#### Accessing Intent Data

When an intent triggers an Intent Received event, the resulting task(s) which are executed have access to many details of the intent via local variables (where relevant and present):

*   _%intent\_data_: the data
*   _%evtprm1_: the action
*   _%evtprm2_: the first category
*   _%evtprm3_: the second category
*   _%evtprm4_: the URI scheme
*   _%evtprm5_: the MIME type

In addition, any _extras_ attached to the intent can be accessed under their name, with the following modifications to make them valid variable names:

*   all letters will be converted to lower-case, then
*   names of length less than 3 will have **var\_** prefixed
*   non-letter-or-digit characters will be converted to \_, then
*   names not starting with a letter will have **a** prefixed, then
*   names not ending with a letter or digit will have **a** affixed
*   if the result is the name of another extra, **\_dup** will be affixed until that is no longer the case

For example, an extra with key **%SOUND\_ON** will be available as **%sound\_on**, and an extra with key **package.SOUND\_ON!**, will be available via the local variable **%package\_sound\_on\_a**

The following extra types are presented in Tasker as local arrays: `String [], Integer [], ArrayList, ArrayList`.

Example: a string array extra \`named 'fruits' with values 'pear' and 'apple' will result in the local variables %fruits1 (=pear) and %fruits2 (=apple).

Java Support ![](icon_tasker.png)
--------------------------------- 

### Introduction

Android has hundreds of thousands of functions which apps can use. It's not possible for Tasker to present all of those to the user, so Tasker allows the advanced user to directly call those Java functions and work with Java objects themselves.

It does **not** allow you to 'write Java code'... but the combination of Tasker's logic and flow control with direct access to the Android API is sufficient for most automation purposes.

This page assumes you have a basic familiarity with the Java concepts of _objects_ and _classes_.

Developer information on the Android API is available from [Google](http://developer.google.com/develop).

#### Example

1.  `Variable Set`, %service, wifi
2.  `Java Function`, wiman = CONTEXT.getSystemService( %service )
3.  `Java Function`, %enabled = wiman.isWifiEnabled()
4.  `Java Function`, wiman.setEnabled( true ), If %enabled eq false

This example task turns wifi on if it is not already enabled.

Action 2 demonstrates that Tasker variables can be used in Java function calls. _wiman_ is a Java object resulting from the function call which is stored by Tasker for use in subsequent actions. _CONTEXT_ is also such a variable but is built-in and always accessible to `Java Function`.

Action 3 demonstrates that results of `Java Function` can also be assigned to Tasker variables. Since all Tasker variables are strings, some conversion needs to take place depending on what type of object the Java function returns. In this case it's a boolean, and so %enabled will be **true** or **false**.

Action 4 demonstrates taking a decision based on the result of previous Java function call.

### The `Java Function` Action

#### Using The Action

*   enter an object or class (to access static functions) into the first parameter.
    
    The magnifying glass icon will show a class selector for classes known in the latest Android API. Some may be coloured red, as not all classes are available on all devices.
    
    The coffee-cup icon allows quick selection of known Java objects
    
    The question mark icon will attempt to link to the relevant Android reference page for the object or class.
    2.  click the magnifying class next to the `Function` parameter to select a function to execute appropriate to the object or class from step 1.
    
    In most cases, Tasker will be able to guess which class an object is, and hence which functions are available, if not, see [casting](#casting) below.
    
    Functions listed in red are private, meaning they can be used, but the author didn't intend them to be.
    
3.  if the function returns a value, you can enter a Java [object name](#names) to assign it to, or a Tasker variable, see [below](#return).
    
4.  enter any parameters required for the function, see [below](#params). The type of object the function expects for the parameter is displayed above the text entry field. The magnifying glass will list any fields associated with the current entry in the text box, where possible.

#### Parameters

If you don't enter a value for a parameter, `null` will be used for that parameter when the function is called.

If you enter the name of a variable array, Tasker will attempt to convert the array values into the type of object (an array or collection) which the function expects.

Other Tasker variables will be replaced in the usual way.

Here can also be entered Java objects, or their fields, either built-in or created by previous calls to `Java Function` (e.g. `wiman` or `arr[0].length`)

#### Return Values

When a Java function returns a value, it can be placed in either a Tasker variable or a Java object (or ignored).

If it's placed into a Tasker variable, it's converted to a piece of text and the object itself is lost and can no longer be accessed. Note that if the Java object is an array or list, it will be assigned to multiple Tasker variables in the usual way e.g. %val1, %val2...

When the returned value is placed into a Java object, you can access the object at a later time in another `Java Function` and some other (see later) actions.

Note that return value classes are inferred from the function, so object names can refer to different classes at different times. It's not recommended to reuse names in this way however!

### Objects

#### Creating An Object

New objects of most types can be created by filling in the class name, hitting the function selector and selecting a function called `new`.

It's worth noting that many classes in the Android API have special static functions for getting a new object of that class called e.g. `getInstance` or similar.

Arrays (also multidimensional) can be created by adding `[]` to the class name (or e.g. `[][]`).

Here's an example of creating a 3x5 string array:

1.  `Java Function`, arr = new String\[\]\[\]( 3 )
2.  `For`, %rowno, 0:2
3.     `Java Function`, arr\[%rowno\] = new String\[\]( 5 )

Creating an array is also possible natively via the `newInstance` function in the the class `Array`.

Array components can be accessed as in normal Java (`arr[0][1]`) wherever Java objects are [supported](#support).

#### Object Naming, Local and Global

Object names can consist of any any combination of upper or lower case letters and underscore and, unlike Tasker variable names, may start with underscore. The first letter may not be upper-case, as this is a convention used to distinguish objects from classes.

Analogous to Tasker variables, Java objects are either local to the current task if their name is all lower case, or global (available to any other task) if there are any upper-case characters in the name. All-upper-case names represent final (fixed) global objects which cannot be modified.

There are three important things to remember about global Java objects:

*   it's important to delete them once they are no longer needed, because they can take up a lot of memory.
*   unlike global Tasker variables, they are lost when Tasker is killed e.g. because the device was restarted
*   their names can only contain upper- or lower-case letters or underscore.

#### Built-in Objects

*   **Android Context** (class `Context`)  
    _CONTEXT_  
    Many funtions in Android require a context object. In tasks running **directly** as a result of a scene element event, this is the Activity object which is displaying the scene, otherwise it's Tasker's Application context.
*   **Image Buffer** (class `Bitmap`)  
    _IBUFFER_ The object manipulated by functions in Tasker's _Image_ action category.  
    

#### Assigning Values

When writing Java code, to make a name refer to the same object as another name, you would use something like:

	`String a = "hello";`
	`String b = a;`

Now both a and b refer to the same object.

To achieve that in Tasker, you use the special `assignTo` function after selecting the object to assign.

	`Java Function, a, "hello", assign` (or `a = "hello".assign()`)
	`Java Function, b, a, assign` (or `b = a.assign()`)

#### Other Actions Supporting Objects

##### If

A Java object can be directly referenced in a condition. Null-value objects are replaced with text representation `null`.

Examples:

	`If, arr[0][0] eq 45`
	`If, arr[0].length > 3` 
	`If, lightlevel Equals null`

You cannot make function calls e.g. str.charAt( 5 )

##### For

The _Value_ parameter in the For action can include Java object references as for _If_.

	`For, %value, arr`

Will repeat once for each value in the array _arr_. This will also work for string lists and simple objects (boolean etc)

### Other Topics

#### Casting

_Casting_ in Tasker is used only to tell Tasker the type of a particular object. That can be useful so that e.g. Tasker can show functions which are appropriate to it.

In the example at the top of the page, the `getSystemService` function returns an Object:

	`Java Function`, wiman = CONTEXT.getSystemService( %service )

Since the object could be one of many kinds of managers, Tasker is not able to list the WifiManager functions for easy selection when creating the next `Java Function` action in the task.

You can tell Tasker the actual type by adding a cast in brackets before the name:

	`Java Function`, (WifiManager) wiman = CONTEXT.getSystemService( %service )

#### Constants

Tasker support the usual naming conventions for Java constants.

*   **L** a long integer e.g. `300L`
*   **F** a floating-point number e.g. `45.6D`
*   **D** a double-length float e.g. `45.6D`
*   **double quotes** indicate a string e.g. `"hello"`, though in many cases Tasker will infer that a string was intended anyway
*   **single quotes** indicate a character e.g. `'x'`

Tasker will attempt to convert numbers without affixes to a Java type in the following order: `int, long, float, double`.

#### Generic Classes

Tasker only supports fully the following generic classes:`   *   ArrayList<String> *   ArrayList<View> *   ArrayList<Bundle> *   ArrayList<Integer> *   ArrayList<Long> *   ArrayList<Double> *   ArrayList<Float>   `

Create them by selecting their class in the class selector, clicking the function selector and clicking _new_.

Generic classes mixed with arrays cannot be handled by Tasker, though you can pass such objects around from function to function.

#### Permissions

For some function calls, Android requires that the calling app have declared a permission otherwise the call will fail. This means that a Java Function call will fail if the permission is not one of the ones pre-declared by Tasker.

Unfortunately, Android does not allow permissions to be added dynamically, so if you wish to use a function requiring a permission that Tasker does not already have, the only option is to generate a child app to run the function (see [App Creation](#appcreation.html)). In the child configuration screen you can add any permissions which your Java Function call needs to the child app.

#### Service Thread

Java code is executed with a non-UI thread by a service.

Some implications are:

*   things which require an activity will not work e.g. showing a dialog
*   sending intents will in some cases require the flag `Intent.FLAG_FROM_BACKGROUND` and possibly also `Intent.FLAG_ACTIVITY_NEW_TASK`

#### Static Fields

Static fields (e.g. `ContentResolver.EXTRA_SIZE`) are not currently supported by Tasker.

A workaround is to use reflection to get (or set) the value:

	`res = CONTEXT.getContentResolver();`
	`cls = res.getClass();`
	`fld = cls.getField( EXTRA_SIZE );`
	`%val = fld.get( null );`

JavaScript Support ![](icon_tasker.png)
--------------------------------------- 

### Introduction

Tasker supports running JavaScript code in tasks or [WebView](#element_web.html) scene elements. Most Tasker actions can be accessed direct from the JavaScript. JSON and XMLHTTPRequest are also directly available from the JavaScript code.

#### JavaScript in Tasks

JavaScript can be embedded inline in tasks via the _JavaScriptlet_ (direct specification of JavaScript to run) or _JavaScript_ (load script from file) actions.

In both cases, the JavaScript executes in sequence with the other actions in the task and variables are transparently converted so pieces of JavaScript can be interwoven throughout the task.

#### Embedded in HTML

WebView elements allow specification of mixed HTML and JS for the element content.

> `<H1 onClick="setWifi( false )">ClickMeToTurnOffWifi</H1>`

This allows a single WebView to present a complete user-interface.

### Local Variables

In `JavaScript(let)` actions, local variables (all lower case, e.g. **%myvar**) are directly accessible in the JavaScript without the % sign (e.g. **myvar**). If the script changes the value, the new value is transparently used by subsequent actions in the task.

The values of new (all lower case) variables declared in JavaScript (with the `var` keyword) are also available to subsequent actions, with the exception of those which are chain-declared e.g. `var one = 'aval', two = 'bval';`

In JavaScript embedded in HTML, the functions [local](#local) and [setLocal](#setLocal) must be used to access variables local to the scene hosting the WebView.

### Global Variables

Tasker global variables need to be accessed via [global()](#global) and set via [setGlobal()](#setGlobal). Global arrays are not supported due to an Android limitation.

### Arrays

Local Tasker arrays are transparently available in _Javascript(let)_s and vice-versa. They are not available in WebViews.

Arrays which are not existing Tasker arrays must be declared in the JS as such i.e. in this case _arr_ will not be visible to the remainder of the task:

	var arr = getSomeArray();

Whereas in this case it will:

	var arr = \[\];
	arr = getSomeArray();

Note that:

*   JavaScript array indices start at 0, whereas Tasker array indices start at 1
*   JavaScript uses `[]` while Tasker uses `()`

So, for example, `%arr(1)` (Tasker) is equivalent to `arr[0]` (JavaScript).

### Settings

Unlike normal Tasker actions, settings which are changed in JavaScript as part of a profile's enter task are **not** restored when the profile exits.

### Execution

#### Execution Instances

Only one script can execute at one time. Once a piece of JavaScript is executing, it cannot be interrupted by another piece.

#### Working Off-Device

You might wish to develop long and/or complicated tasks off-device e.g. on a PC. There are two strategies for that:

#### 1\. `JavaScript` action

For off-device testing, use `Menu / More / Developer / Save JS Library Template` to get dummy definitions for the built in functions. Include that file when developing on your PC.

To test in your JavaScript code whether you're on-device or not, use

> `var onAndroid = ( global( 'sdk' ) > 0 );`

By using the `JavaScript` action rather than `JavaScriptlet` you can easily access a file synced from PC to a file on the Android device.

#### 2\. Using WebView

If you specify a website URL as the content for your WebView, then testing the code on the target device is a simple matter of pushing the new version to your webserver and reloading the WebView on the device (see action [Element Web Control](#help/ah_scene_element_web_control.html))

#### Builtin Function Execution

Calls to most Tasker builtin functions (see below) are executed as normal single-action tasks and thus may be blocked by other executing tasks.

They execute at the priority of the task that executed the JavaScript **plus two**.

#### JavaScript(let): Alert,Confirm,Prompt

Scripts using these functions require a 'user-interface' and may cause interference with the currently running app (though in most cases they will not).

#### JavaScript(let): Auto Exit

By default, the `JavaScript(let)` action will end when the main execution sequence is finished.

If you are using asynchronous code e.g. via _setTimeout()_ or other callbacks, you should deselect _Auto Exit_. You are then responsible yourself for telling Tasker to continue the task by calling _exit()_.

In any case, execution will stop when the timeout configured for the action is reached.

#### JavaScript(let): Libraries

You can specify as many libraries as you want in the _Libraries_ parameter, separated by newlines.

Several popular libraries are pre-selectable.

You may wish to download them manually to your local storage and change the _http_ URL to a _file_ URL so that Internet is not required to run your script.

Warning: library code will have access to local files, data providers etc. on the device

Important: if you are using your own libraries developed on Windows, you may need to convert CRLF style line endings to Unix style LF.

### Builtin Functions

Tasker makes most of it's actions available via functions which can be called directly via name in `JavaScript(let)` actions and WebView elements.

Exceptions:

*   in WebView content where mode is set to **URL**, the functions must be prefixed by **tk** e.g. `tk.flash('Woo!')`
*   when executing code via _eval_ the functions must be prefixed by **tk.**

##### alarmVol / btVoiceVol / callVol / dtmfVol / mediaVol / notificationVol / systemVol / ringerVol

`var ok = alarmVol( int level, bool display, bool sound )`

Set the relevant system volume to _level_.

If _display_ is true, the new level will be flashed up on-screen.

If _sound_ is true, a tone will sound at the new level.

##### audioRecord

`var ok = audioRecord( str destPath, str source, str codec, str format )`

*   _destPath_: where to put the recording. Note that a file extension is not necessary, it will correspond to the selected _format_.
*   _source_: **def, mic, call, callout** or **callin**
*   _codec_: **amrn, amrw** or **aac**
*   _format_: **mp4, 3gpp, amrn** or **amrw**

The JavaScript does **not** wait for the audio recording to complete.

See also: [audioRecordStop()](#audioRecordStop).

##### audioRecordStop

`var ok = audioRecordStop()`

Stop recording previously initiated by [audioRecord()](#audioRecord).

##### browseURL

`var ok = browseURL( str URL )`

Open the default browser at the specifed URL.

##### button

`var ok = button( str name )`

Simulate a press of the named button.

_name_ must be one of **back, call, camera, endcall, menu, volup, voldown** or **search**.

This function requires a rooted device.

##### call

`var ok = call( str num, bool autoDial )`

Make a phone call.

If _autoDial_ is **false**, the phone app will be brought up with the number pre-inserted, if **true** the number will also be dialed.

##### callBlock

`var ok = callBlock( str numMatch, bool showInfo )`

Block **outgoing** calls [matching](#matching.html) _numMatch_.

If _showInfo_ is set, Tasker will flash a message when a call is blocked.

##### callDivert

`var ok = callDivert( str fromMatch, str to, bool showInfo )`

Divert **outgoing** calls [matching](#matching.html) _fromMatch_ to the number _to_.

If _showInfo_ is set, Tasker will flash a message when a call is diverted.

##### callRevert

`var ok = callRevert( str numMatch )`

Stop blocking or diverting outgoing calls previously specified with [callBlock](#callBlock) or [callDivert](#callDivert).

##### carMode

`var ok = carMode( bool onFlag )`

Turn on or off Android Car Mode.

##### clearKey

`var ok = clearKey( str keyName )`

Clear the passphrase for the specified _keyName_.

See Also: [Encryption](#encryption.html) in the Userguide.

##### composeEmail

`var ok = composeEmail( str to, str subject, str message )`

Show an email composition dialog with any specified fields pre-filled.

The JavaScript does **not** wait for the email to be sent before continuing.

##### composeMMS

`var ok = composeMMS( str to, str subject, str message, str attachmentPath )`

Show an MMS composition dialog with any specified fields pre-filled.

The JavaScript does **not** wait for the MMS to be sent before continuing.

##### composeSMS

`var ok = composeSMS( str to, str message )`

Show an SMS composition dialog with any specified fields pre-filled.

The JavaScript does **not** wait for the SMS to be sent before continuing.

##### convert

`var result = convert( str val, str conversionType )`

Convert from one type of value to another.

_conversionType_ must be one of the string constants: **byteToKbyte, byteToMbyte, byteToGbyte, datetimeToSec, secToDatetime, secToDatetimeM, secToDatetimeL, htmlToText, celsToFahr, fahrToCels, inchToCent, metreToFeet, feetToMetre, kgToPound, poundToKg, kmToMile, mileToKm, urlDecode, urlEncode, binToDec, decToBin, hexToDec, decToHex, base64encode base64decode, toMd5, toSha1, toLowerCase, toUpperCase, toUpperCaseFirst**.

See also: action [Variable Convert](#help/ah_convert_variable.html).

##### createDir

`var ok = createDir( str dirPath, bool createParent, bool useRoot )`

Create the named _dirPath_. If _createParent_ is specified and any parent directory does not exist, it will also be created.

If _useRoot_ is specified, the operation will be performed as the root user (where available).

##### createScene

`var ok = createScene( str sceneName )`

Create the named [scene](#scenes.html) without displaying it.

##### cropImage

`var ok = cropImage( int fromLeftPercent, int fromRightPercent, int fromTopPercent, int fromBottomPercent )`

Crop an image in Tasker's image buffer previously loaded via [loadImage](#loadImage).

##### decryptDir

`var ok = decryptDir( str path, str key, bool removeKey )`

As [decryptFile()](#decryptFile), but decrypts each file in the specified directory in turn.

##### decryptFile

`var ok = decryptFile( str path, str key, bool removeKey )`

Decrypt the specified file using the encryption parameters specified in `Menu / Prefs / Action`.

If _removeKey_ is not set, the entered passphrase will be reapplied automatically to the next encryption/decryption operation with the specified _keyName_.

See Also: [Encryption](#encryption.html) in the Userguide, [Decrypt File](#help/ah_decrypt_file.html) action.

##### deleteDir

`var ok = deleteDir( str dirPath, bool recurse, bool useRoot )`

Delete the named _dirPath_. _recurse_ must be specified if the directory is not empty.

If _useRoot_ is specified, the operation will be performed as the root user (where available).

##### deleteFile

`var ok = deleteFile( str filePath, int shredTimes, bool useRoot )`

Delete the named _filePath_.

_shredTimes_ has range 0-10.

If _useRoot_ is specified, the operation will be performed as the root user (where available).

See also: action [Delete File](#help/ah_delete_file.html)

##### destroyScene

`var ok = destroyScene( str sceneName )`

Hide the named [scene](#scenes.html) if it's visible, then destroy it.

##### displayAutoBright

`var ok = displayAutoBright( bool onFlag )`

Whether the display brightness should automatically adjust to the ambient light or not.

##### displayAutoRotate

`var ok = displayRotate( bool onFlag )`

Whether the display orientation should change based on the physical orientation of the device.

##### displayTimeout

`var ok = displayTimeout( int hours, int minutes, int seconds )`

How long the period of no-activity should be before the display is turned off.

##### dpad

`var ok = dpad( str direction, int noRepeats )`

Simulate a movement or press of the hardware dpad (or trackball).

_direction_ must be one of **up, down, left, right** or **press**.

This function requires a rooted device.

##### enableProfile

`var ok = enableProfile( str name, boolean enable )`

Enable or disable the named Tasker profile.

##### encryptDir

`var ok = encryptDir( str path, str keyName, bool rememberKey, bool shredOriginal )`

As [encryptFile()](#encryptFile), but encrypts each file in the specified directory in turn.

##### elemBackColour

`var ok = elemBackColour( str scene, str element, str startColour, str endColour )`

Set the background [colour](#colour) of the specified [scene](#scenes.html) element.

See also: action [Element Back Colour](#help/ah_scene_element_background_colour.html).

##### elemBorder

`var ok = elemBorder( str scene, str element, int width, str colour )`

Set the border [colour](#colour) and width of the specified [scene](#scenes.html) element.

##### elemPosition

`var ok = elemPosition( str scene, str element, str orientation, int x, int y, int animMS )`

Move an element within it's scene.

_orientation_ must be one of **port** or **land**. _animMS_ indicates the duration of the corresponding animation in MS. A zero-value indicates no animation.

See also: action [Element Position](#help/ah_scene_element_position.html).

##### elemText

`var ok = elemText( str scene, str element, str position, str text )`

Set the text of the specified [scene](#scenes.html) element.

_pos_ must be one of **repl** (replace existing text completely), **start** (insert before existing text) or **end** (append after existing text).

See also: action [Element Text](#help/ah_scene_element_text.html).

##### elemTextColour

`var ok = elemTextColour( str scene, str element, str colour )`

Set the text [colour](#colour) of the specified [scene](#scenes.html) element.

See also: action [Element Text Colour](#help/ah_scene_element_text_colour.html).

##### elemTextSize

`var ok = elemTextSize( str scene, str element, int size )`

Set the text size of the specified [scene](#scenes.html) element.

See also: action [Element Text Size](#help/scene_element_text_size.html).

##### elemVisibility

`var ok = elemVisibility( str scene, str element, boolean visible, int animationTimeMS )`

Make the specified [scene](#scenes.html) element visible or invisible.

See also: action [Element Visibility](#help/ah_scene_element_visibility.html).

##### endCall

`var ok = endCall()`

Terminate the current call (if there is one).

##### encryptFile

`var ok = encryptFile( str path, str keyName, bool rememberKey, bool shredOriginal )`

Encrypt the specified file using the encryption parameters specified in `Menu / Prefs / Action`.

If _rememberKey_ is set, the entered passphrase will be reapplied automatically to the next encryption/decryption operation with the specified _keyName_.

If _shredOriginal_ is specified, the original file will be overwritten several times with random bits if encryption is successful.

See Also: [Encryption](#encryption.html) in the Userguide, [Encrypt File](#help/ah_encrypt_file.html) action.

##### enterKey

`var ok = enterKey( str title, str keyName, bool showOverKeyguard, bool confirm, str background, str layout, int timeoutSecs )`

Show a dialog to enter the passphrase for the specified _keyName_. The JavaScript waits until the dialog has been dismissed or the timeout reached.

*   _confirm_: if set, the passphrase must be entered twice to ensure it is correct.
*   _background_: \[optional\] a file path or file URI to a background image.*   _layout_: the name of a user-created [scene](#scenes.html) to use in place of the built-in scene.

See Also: [Encryption](#encryption.html) in the Userguide

##### filterImage

`bool ok = filterImage( str mode, int value )`

Filter an image previously loaded into Tasker's image buffer via [loadImage()](#loadImage)

Possible values of _mode_ are:

*   **bw**: convert to black & white, using _value_ as a threshold
*   **eblue**: enhance blue values by _value_
*   **egreen**: enhance green values by _value_
*   **ered**: enhance red values by _value_
*   **grey**: convert to greyscale, _value_ is unused
*   **alpha**: set pixel alpha (opposite of transparency) to _value_

_value_ should be 1-254.

##### flipImage

`bool ok = flipImage( bool horizontal )`

Flip an image previously loaded into Tasker's image buffer via [loadImage()](#loadImage)

If _horizontal_ is false, the image is flipped vertically.

##### exit

`exit()`

Stop execution of the JavaScript.

##### flash

`flash( str message )`

Flash a short-duration Android 'Toast' message.

##### flashLong

`flashLong( str message )`

Flash a long-duration Android 'Toast' message.

##### getLocation

`var ok = getLocation( str source, bool keepTracking, int timeoutSecs )`

Try to get a fix of the current device location.

_source_ must be one of **gps, net** or **any**.

If _keepTracking_ is set, the specified source(s) will be left tracking with the purpose of providing a much quicker fix next time the function is called.

Fix coordinates are stored in the global Tasker variables **%LOC** (GPS) and/or **%LOCN** (Net). The value can be retrieved with the [global](#global) function. Several other parameters of the fix are also available, see [Variables](#variables.html).

Example

    
    	var lastFix = global( 'LOC' );
    	if ( 
    		getLocation( 'gps' ) &&
    		( global( 'LOC' ) != lastFix ) 
    	) {
    		flash( "New fix: " + global( 'LOC' ) );
    	}
    

See also: action [Get Location](#help/ah_get_fix.html), function [stopLocation](#stopLocation).

##### getVoice

`str result = getVoice( str prompt, str languageModel, int timeout )`

Get voice input and convert to text.

_result_ is 'undefined' if the voice acquisition failed, otherwise it's an array of possible matching texts.

_prompt_ is a label for the dialog that is shown during voice acquisition.

_languageMode_ gives the speech recognition engine a clue as to the context of the speech. It must be one of **web** for 'web search' or **free** for 'free-form'.

##### goHome

`goHome( int screenNum )`

Go to the Android home screen. _screenNum_ is not supported by all home screens.

##### haptics

`var ok = haptics( bool onFlag )`

Enable/disable system setting Haptic Feedback.

##### hideScene

`var ok = hideScene( str sceneName )`

Hide the named [scene](#scenes.html) if it's visible.

##### global

`var value = global( str varName )`

Retrieve the value of a Tasker global variable. Prefixing the name with % is optional.

Example:

    
    	flash( global( '%DogName' ) );
##### listFiles

`str files = listFiles( str dirPath, bool hiddenToo )`

List all files in the specified _dirPath_.

_files_ is a newline-separated list of subfiles.

If no files or found or an error occurs, the returned value will be `undef`.

If _hiddenToo_ is specified, files starting with period are included, otherwise they are not.

Example:

	var files = listFiles( '/sdcard' );
	var arr = files.split( '\\n' );
	flash( 'Found ' + arr.length + ' files' );

##### loadApp

`var ok = loadApp( str name, str data, bool excludeFromRecents )`

Start up the named app.

_Name_ can be a package name or app label, it's tested first against known package names. **Note**: app label could be localized to another language if the script is used in an exported app.

_Data_ is in URI format and app-specific.

When _excludeFromRecents_ is true, the app will not appear in the home screen 'recent applications' list.

##### loadImage

`var ok = loadImage( str uri )`

Load an image into Tasker's internal image buffer.

The following uri formats are currently supported:

*   _file://_ followed by a local file path

See also [Load Image](#help/ah_load_image.html) action.

##### lock

`var ok = lock( str title, str code, bool allowCancel, bool rememberCode, bool fullScreen, str background, str layout )`

Show a lock screen, preventing user interaction with the covered part of the screen. The JavaScript waits until the code has been entered or the lock cancelled (see below).

*   _code_: the numeric code which must be entered for unlock
*   _allowCancel_: show a button to remove the lockscreen, which causes a return to the Android home screen
*   _rememberCode_: the code will be remembered and automatically entered when the lock screen is show in future, until the display next turns off
*   _background_: \[optional\] a file path or file URI to a background image.*   _layout_: the name of a user-created [scene](#scenes.html) to use in place of the built-in lock scene

##### local

`var value = local( str varName )`

Retrieve the value of a Tasker scene-local variable. The name should **not** be prefixed with _%_.

This function is only for use by JavaScript embedded in HTML and accessed via a WebView scene element.

##### mediaControl

`var ok = mediaControl( str action )`

Control media via simulation of hardware buttons.

Possible _action_s are **next, pause, prev, toggle, stop** or **play**.

##### micMute

`var ok = micMute( bool shouldMute )`

Mute or unmute the device's microphone (if present),

##### mobileData

`var ok = mobileData( bool set )`

Enable or disable the system Mobile Data setting.

See also: action [Mobile Data](#help/ah_mobile_data_direct.html)

##### musicBack

`var ok = musicBack( int seconds )`

Skip back by _seconds_ during playback of a music file previously started by [musicPlay](#musicPlay).

See also: [musicSkip](#musicSkip), [musicStop](#musicStop)

##### musicPlay

`var ok = musicPlay( str path, int offsetSecs, bool loop, str stream )`

Play a music file via Tasker's internal music player.

_stream_ to which [audio stream](#streams) the music should be played

This function does **not** not wait for completion.

The last 3 arguments may be ommitted, in which case they default to **0**, **false** and **media** respectively.

See also: [musicStop](#musicStop), [musicBack](#musicBack), [musicSkip](#musicSkip)

##### musicSkip

`var ok = musicSkip( int seconds )`

Skip forwards by _seconds_ during playback of a music file previously started by [musicPlay](#musicPlay).

See also: [musicBack](#musicBack), [musicStop](#musicStop)

##### musicStop

`var ok = musicStop()`

Stop playback of a music file previously started by [musicPlay](#musicPlay).

See also: [musicBack](#musicBack), [musicSkip](#musicSkip)

##### nightMode

`var ok = nightMode( bool onFlag )`

Turn on or off Android Night Mode.

##### popup

`var ok = popup( str title, str text, bool showOverKeyguard, str background, str layout, int timeoutSecs )`

Show a popup dialog. The JavaScript waits until the popup has been dismissed or the timeout reached.

*   _background_: \[optional\] a file path or file URI to a background image.*   _layout_: the name of a user-created [scene](#scenes.html) to use in place of the built-in popup scene.

##### performTask

`var ok = performTask( str taskName, int priority, str parameterOne, str parameterTwo )`

Run the Tasker task _taskName_.

Note that the JavaScript does not wait for the task to complete.

##### profileActive

`bool active = profileActive( str profileName )`

Whether the named Tasker profile is currently active. Returns false if the profile name is unknown.

##### pulse

`bool ok = pulse( bool onFlag )`

Enable or disable the Android Notification Pulse system setting.

##### readFile

`var contents = readFile( str path )`

Read the contents of a text file.

##### reboot

`var ok = reboot( str type )`

Reboot the device.

_type_ is one of **normal, recovery** or **bootloader**. It can be ommitted and defaults to **normal**.

Requires a rooted device.

See also: function [shutdown](#shutdown)

##### resizeImage

`var ok = resizeImage( int width, int height )`

Scale the current image in Tasker's image buffer to the specified dimensions.

##### rotateImage

`var ok = rotateImage( str dir, int degrees )`

Rotate the current image in Tasker's image buffer.

_dir_ must be one of **left** or **right**. _degrees_ must be one of **45, 90, 135** or **180**.

##### saveImage

`var ok = saveImage( str path, int qualityPercent, bool deleteFromMemoryAfter )`

Save the current image in Tasker's image buffer to the specified file _path_.

[Save Image](#help/ah_save_image.html) action.

##### say

`var ok = say( str text, str engine, str voice, str stream, int pitch, int speed )`

Cause the device to say _text_ out loud.

*   _engine_: the speech engine e.g. **com.svox.classic** Defaults to the system default (specify _undefined_ for that)
*   _voice_: the voice to use (must be supported by _engine_). Defaults to the current system language (specify _undefined_ for that)*   _stream_: to which [audio stream](#streams) the speech should be made
*   _pitch_: 1-10
*   _speed_: 1-10

The script waits for the speech to be finished.

##### sendIntent

`var ok = sendIntent( str action, str targetComp, str package, str class, str category, str data, str mimeType, str[] extras );`

Send an intent. Intents are Android's high-level application interaction system.

Any parameter may be specified as undefined.

*   _targetComp_: the type of application component to target, one of **receiver, activity** or **service**. Defaults to **receiver**.
*   _package_: the application package to limt the intent to
*   _class_: the application class to limit the intent to
*   _category_: one of **none, alt, browsable, cardock, deskdock, home, info, launcher, preference, selectedalt, tab** or **test**, defaults to **none**
*   _extras_: extra data to pass, in the format key:value. May be undefined. Maximum length 2.

See also: action [Send Intent](#help/ah_send_intent.html).

##### sendSMS

`var ok = sendSMS( str number, str text, boolean storeInMessagingApp );`

Send an SMS.

See also: action [Send SMS](#help/ah_send_sms.html)

##### setAirplaneMode

`var ok = setAirplaneMode( bool setOn )`

Enable or disable Airplane Mode.

Get the current value with:

`var enabled = global( 'AIR' );`

See also: function [setAirplaneRadios](#setAirplaneRadios)

##### setAirplaneRadios

`var ok = setAirplaneRadios( str disableRadios )`

Specify the radios which will be **disabled** when the device enters Airplane Mode.

_disableRadios_ is a comma-separated list with radio names from the following set: **cell, nfc, wifi, wimax, bt**.

Get the current value with:

`var radios = global( 'AIRR' );`

See also: function [setAirplaneMode](#setAirplaneMode)

##### setAlarm

`var ok = setAlarm( int hour, int min, str message, bool confirmFlag )`

Create an alarm in the default alarm clock app.

_confirmFlag_ specifies whether the app should confirm that the alarm has been set.

_message_ is optional.

Requires Android version 2.3+.

##### setAutoSync

`var ok = setAutoSync( bool setOn )`

Enable or disable the global auto-sync setting.

##### scanCard

`var ok = scanCard( str path )`

Force the system to scan the external storage card for new/deleted media.

If _path_ is defined, only that will be scanned.

See also: action [Scan Card](#help/ah_scan_card.html)

##### setBT

`var ok = setBT( bool setOn )`

Enable or disable the Bluetooth radio (if present).

Test BT state with:

`if ( global( 'BLUE' ) == "on" ) { doSomething(); }`

##### setBTID

`var ok = setBTID( str toSet )`

Set the bluetooth adapter ID (the name as seen by other devices).

##### setGlobal

`setGlobal( str varName, str newValue )`

Set the value of a Tasker global user variable. Prefixing varName with % is optional.

Arrays are **not** supported due to limitations of the Android JS interface.

##### setKey

`var ok = setKey( str keyName, str passphrase )`

Set the passphrase for the specified _keyName_.

See Also: [Encryption](#encryption.html) in the Userguide.

##### setLocal

`setLocal( str varName, str newValue )`

Set the value of a Tasker **scene-local** user variable. Variable names should **not** be prefixed with _%_.

This function is only for use by JavaScript embedded in HTML and accessed via a WebView scene element.

##### setClip

`var ok = setClip( str text, bool appendFlag )`

Set the global system clipboard.

Test the value with:

`var clip = global( 'CLIP' );`

##### settings

`var ok = settings( str screenName )`

Show an Android System Settings screen.

_screenName_ must be one of **all, accessibility, addacount, airplanemode, apn, app, batteryinfo, appmanage bluetooth, date, deviceinfo, dictionary, display, inputmethod, internalstorage, locale, location, memorycard, networkoperator, powerusage, privacy, quicklaunch, security, mobiledata, search, sound, sync, wifi, wifiip** or **wireless**.

##### setWallpaper

`var ok = setWallpaper( str path )`

Set the system home screen wallpaper.

##### setWifi

`var ok = setWifi( bool setOn )`

Enable or disable the Wifi radio (if present).

Test wifi state with:

`if ( global( 'WIFI' ) == "on" ) { doSomething(); }`

##### shell

`var output = shell( str command, bool asRoot, int timoutSecs )`

Run the shell command _command_.

_asRoot_ will only have effect if the device is rooted.

_output_ is 'undefined' if the shell command failed. It's maximum size is restricted to around 750K.

##### showScene

`var ok = showScene( str name, str displayAs, int hoffset, int voffset, bool showExitIcon, bool waitForExit )`

Show the named [scene](#scenes.html), creating it first if necessary.

*   _displayAs_: options: `Overlay, OverBlocking, OverBlockFullDisplay, Dialog, DialogBlur, DialogDim, ActivityFullWindow, ActivityFullDisplay, ActivityFullDisplayNoTitle`
*   _hoffset, voffset_: percentage vertical and horizontal offset for the scene -100% to 100% (not relevant for full screen/window display types)
*   _showExitIcon_: display a small icon in the bottom right which destroys the scene when pressed
*   _waitForExit_: whether to wait for the scene to exit before continuing the script

##### shutdown

`var ok = shutdown()`

Shutdown the device.

Requires a rooted device.

See also: [reboot](#reboot)

##### silentMode

`var ok = silentMode( str mode )`

Set the system silent ('ringer') mode.

_mode_ must be one of **off, vibrate** or **on**

##### sl4a

`var ok = sl4a( str scriptName, boolean inTerminal )`

Run a previously created [SL4A](https://code.google.com/p/android-scripting/) script.

##### soundEffects

`var ok = soundEffects( bool setTo )`

Setting the system _Sound Effects_ setting (sound from clicking on buttons etc.

##### speakerphone

`var ok = speakerPhone( bool setFlag )`

Enable or disable the speakerphone function.

##### statusBar

`var ok = statusBar( bool expanded )`

Expand or contract the system status bar.

##### stayOn

`var ok = stayOn( str mode )`

Specify whether the device should remain on when power is connected.

Possible _mode_s are **never, ac, usb, any**.

##### stopLocation

`var ok = stopLocation()`

Stop tracking a location provider. This is only relevant when a [getLocation](#getLocation) function has been previously called with the _keepTracking_ parameter set.

##### systemLock

`var ok = systemLock()`

Turn off the display and activate the keyguard.

Requires Tasker's Device Administrator to be enabled in Android settings.

##### taskRunning

`bool running = taskRunning( str taskName )`

Whether the named Tasker task is currently running. Returns false if the task name is unknown.

##### takeCall

`bool ok = takeCall();`

Auto-accept an incoming call (if there is one).

##### takePhoto

`bool ok = takePhoto( int camera, str fileName, str resolution, bool insertGallery )`

Take a photo with the builtin camera.

*   _camera_: 0 = rear camera, 1 = front camera
*   _resolution_: format WxH e.g. 640x840
*   _insertGallery_: whether to insert the resulting picture in the Android Gallery application

See also: action [Take Photo](#help/ah_take_photo.html)

##### type

`var ok = type( str text, int repeatCount )`

Simulate keyboard typing.

Requires a rooted device.

##### unzip

`boolean ok = unzip( str zipPath, bool deleteZipAfter )`

Unpack a Zip archive into the parent directory of the archive.

_deleteZip_ causes the zip archive to be deleted after successful unpacking.

##### usbTether

`usbTether( bool set )`

Enable or disable USB tethering.

See also: action [USB Tether](#help/ah_tether_usb.html)

##### vibrate

`vibrate( int durationMilliseconds )`

Cause the device to vibrate for the specified time.

##### vibratePattern

`vibratePattern( str pattern )`

Cause the device to vibrate following the specified _pattern_, which consists of a sequence of off then on millisecond durations e.g.

`500,1000,750,1000`

wait for 500ms, vibrates 1000ms, wait for 750ms, then vibrate for 1000ms.

##### wait

`wait( int durationMilliseconds )`

Pause the script for the specified time.

Warning: may cause some preceeding functions not to complete in some situations. If in doubt, use JavaScript setTimeout() instead.

##### wifiTether

`var ok = wifiTether( bool set )`

Enable or disable Wifi tethering.

See also: action [Wifi Tether](#help/ah_tether_wifi.html)

##### writeFile

`var ok = writeFile( str path, str text, bool append )`

Write _text_ to file _path_.

If _append_ is specified, the text will be attached to the end of the existing file contents (if there are any).

##### zip

`boolean ok = zip( str path, int level, bool deleteOriginalAfter )`

Zip a file or directory.

_level_ is the desired compression level from 1-9, with 9 resulting in the smallest file and the longest compression time.

_deleteOriginal_ causes _path_ to be deleted if the zip operation is successful.

### Notes

#### Audio Streams

Must be one of **call, system, ringer, media, alarm** or **notification**

#### Colours

Colours are specified in _AARRGGBB_ hexadecimal format, with solid white being **FFFFFFFF**.

#### File Paths

File paths can be specified as either absolute (start with **/**) or relative (don't start with **/**).

Relative file paths are relative to the root of the internal storage media. So, for example, `pics/me.jpg` might resolve to `/sdcard/pics/me.jpg`.

Location Without Tears ![](icon_tasker.png)
------------------------------------------- 

This is an overview guide to choosing a method for fixing your location with Tasker. At the end are some [advanced power-saving strategies](#adv).

Power / Accuracy Comparison
---------------------------

| Method               | Power Usage | Accuracy      | Network | Wifi | BT |
| -------------------- | ----------- | ------------- | ------- | ---- | -- |
| State: Cell Near     | \*          | \*            |         |      |    |
| State: BT Near       | \*\*        | \*\*\*\*\*    |         |      | Y  |
| Location: Net        | \*\*        | \*\*          | Y       |      |    |
| Location: Net & Wifi | \*\*\*      | \*\*\*\*\*\*  | Y       | Y    |    |
| State: Wifi Near     | \*\*\*\*    | \*\*\*\*\*    |         | Y    |    |
| Location: GPS        | \*\*\*\*\*  | \*\*\*\*\*    | Y       |      |    |

More stars mean higher power usage or higher accuracy.

Pattern Matching ![](icon_tasker.png)
-------------------------------------

### What's Pattern Matching ?

With Pattern Matching, you specify a _pattern_ which tells Tasker what text you wish to match. For instance, if you want to match any telephone number starting with **0135**, you can specify the simple match **0135\***. **\*** is a special character which _matches_ any number of any character.

Tasker has two type of matching, [Simple Matching](#simple) and more advanced [Regex Matching](#regex).

### Simple Matching

Simple matching is designed to be easy for non-technical people to use.

#### Where's It Used ?

Simple Matching is used in the following places:

*   in the **If** condition of an action, when the **~** (match) or **!~** (not match) operators are specified.
*   in text paremeters of State and Event contexts
*   some other places :-)

#### Matching Rules

*   if a pattern is left blank, it will match against anything
*   if it is not blank it must match the whole target text
*   **/** means 'or', it divides up multiple possible matches
*   a **\*** will match any number of any character. It's not possible to specifically match a **\*** character.
*   a **+** will match one or more of any character. It's not possible to specifically match a **+** character.  
    Beware: the condition '%var matches +' will be **true** if %var has not been assigned a value, because Tasker does not replace variables which do not have a value.
*   matching is case-insensitive (_magic_ will match with _MagiC_) **unless** the pattern contains an upper-case letter e.g. _Magic\*_ will not match against _magically_, but it will match against _Magic Roundabout_
*   a **!** at the very start of a match means **not** e.g. _!\*Magic\*/\*Yellow\*_ matches anything **not** containing the words _Magic_ or _Yellow_
*   it is not possible to specifically match a **!** character at the start of a target (but you could use **\*!**

Examples

*   _help_ matches _help_ but not _helper_.
*   _help\*_ matches _helper_
*   _\*the\*_ matches _the_ (anywhere)
*   _123+_ matches _123_ and minimally one more character
*   _+_ matches anything with at least one character (non-empty)
*   _the\*way_ matches _the other way_ and _the first way_, amongst others
*   _Help/\*shell_ matchs _Help_ or anything ending with _shell_, case-sensitively

#### Caller Matching

Caller matching (some events and states e.g. _Call_) is handled slightly differently.

*   _C:ANY_ matches the telephone number of any contact
*   _C:FAV_ matches the telephone number of any favourite (starred) contact
*   _CG:`groupmatch`_ matches the telephone number of a contact in a group which matches `groupmatch`
*   _Otherwise:_ otherwise a match is attempted using the general matching rules against **both** the caller phone number and the associated contact's name (if there is one).

Examples:

*   _!C:ANY_ matches a number **not** belonging to a contact
*   _077\*/Geoff\*_ matches a number starting with _077_ or belonging to a contact whose names starts with _Geoff_
*   _C:FAV/0123456789_ matches any favourite contact or the telephone number _0123456789_
*   _CG:\*Family\*/CG:Business_ matches any contact in the contact groups _Family Members_, _My Family_ or _Business_

### Regular Expression Matching

Regular expressions are similar to simple matching patterns but have many more features and are much harder for non-technical people.

#### Where's It Used ?

Regex Matching is available:

*   in the **If** condition of an action, when the **~R** or **!~R** operators are specified.
*   in the _Variable Search Replace_ action
*   in the condition of a _Variable Value_ state
*   wherever a Simple Match is possible, by preceding the regex with **~R** or **!~R**

#### Matching Rules

Standard Java regular expression matching is applied. The Android Developer site has a [reference page](http://developer.android.com/reference/java/util/regex/Pattern.html).Maths ![](icon_tasker.png)

#### Where Is Maths Used ?

*   When you do `Variable Set` and click the _Do Maths_ checkbox
*   With the `If` action, if you select a mathematical comparison like **<** or **\=**
*   With individual action conditions when a mathematical comparison is selected

#### What's Available

Tasker uses the [MathEval](http://www.softwaremonkey.org/Code/MathEval) library by Lawrence PC Dol.

#### Operators

*   **\+ - \* /** - the basic operators
*   **%** - modulus
*   **^** - power

##### Constants

*   **E** - the base of the natural logarithms
*   **EUL** - Euler's Constant
*   **LN2** - log of 2 base e
*   **LN10** - log of 10 base e
*   **LOG2E** - log of e base 2
*   **LOG10E** - log of e base 10
*   **PHI** - the golden ratio
*   **PI** - the ratio of the circumference of a circle to its diameter

##### Functions

Trigonometric functions expect a value in radians.

Functions take their argument in parenthesis e.g. sin(torad((90))

*   **abs** - absolute value
*   **acos** - arc cosine; the returned angle is in the range 0.0 through pi
*   **asin** - arc sine; the returned angle is in the range -pi/2 through pi/2
*   **atan** - arc tangent; the returned angle is in the range -pi/2 through pi/2
*   **cbrt** - cube root
*   **ceil** - smallest value that is greater than or equal to the argument and is an integer
*   **cos** - trigonometric cosine
*   **cosh** - hyperbolic cosine
*   **exp** - Euler's number e raised to the power of the value
*   **expm1** - _e_x\-1
*   **floor** - largest value that is less than or equal to the argument and is an integer
*   **getExp** - unbiased exponent used in the representation of val
*   **log** - natural logarithm (base e)
*   **log10** - base 10 logarithm
*   **log1p** - natural logarithm of (val+1)
*   **nextup** - floating-point value adjacent to val in the direction of positive infinity
*   **round** - closest 64 bit integer to the argument
*   **roundhe** - double value that is closest in value to the argument and is equal to a mathematical integer, using the half-even rounding method.
*   **signum** - signum function of the argument; zero if the argument is zero, 1.0 if the argument is greater than zero, -1.0 if the argument is less than zero
*   **sin** - trigonometric sine
*   **sinh** - hyperbolic sine
*   **sqrt** - correctly rounded positive square root
*   **tan** - trigonometric tangent
*   **tanh** - hyperbolic tangent
*   **todeg** - converts an angle measured in radians to an approximately equivalent angle measured in degrees
*   **torad** - converts an angle measured in degrees to an approximately equivalent angle measured in radians
*   **ulp** - size of an ulp of the argument

Variables ![](icon_tasker.png)
------------------------------

#### General

A variable is a named value which changes over time e.g. the level of the battery, the time of day.

When Tasker encounters a variable name in a text, it replaces the name with the current value of the relevant variable before carrying out the action.

The main purposes of variables are:

*   _dynamic binding_: doing something with an action with data which
    
    is unknown when the task is created e.g. respond to an SMS; the sender is not known until the SMS is received.*   allow [flow control](#flowcontrol.html) within and between tasks
*   record data for some future use e.g. passing data between tasks

#### Global vs. Local Variables

Variables which have an **all-lower-case** name (e.g. %fruit\_bar) are _local_, meaning that their value is specific to the task or scene in which they are used.

Variables which have one or more capital letters in their name (e.g. %Car, %WIFI) are _global_, meaning that wherever they are accessed from the same value is returned.

#### Built-In Variables

The values of built-In variables are updated automatically by Tasker.

##### Local Built-In Variables

*   **Action Error**  
    _%err_  
    Is set to an integer if an error occurred when running the last action. The actual number can signify the error which occurred, but is usually 1 for most Tasker actions (notable exception: `Run Shell` and plugins).
*   **Action Error Description**  
    _%errmsg_  
    A description of the error which **last resulted in %err being set**. Currently never set by Tasker but possibly by some plugin actions.
*   **Task Priority**  
    _%priority_  
    The priority of the running task. The priority determines which task executes its next action when several tasks are running together.  
    See also: [Task Scheduling](#scheduling)
*   **Task Queue Time**  
    _%qtime_  
    How long (seconds) the running task has been running.  
    Note that tasks can be interrupted by higher priority tasks, so this number is not necessarily the total run-time of the task.  
    
*   **Task Caller**  
    _%caller_  
    A variable array tracing the origin of the current running task. _%caller1_ gives the origin of the current task, _%caller2_ the origin of _%caller1_ etc.
    
    Example: if task A uses action `Perform Task` to start task B, then when task A is run by pressing the Play button in the task edit screen, _%caller1_ in task B will show **task=A**, _%caller2_ will show **ui**.
    
    The format of each entry in the array is _callertype_(**\=**_callername_(**:**_subcallername_))
    
    Caller types ares detailed below:
    
    *   **profile**  
        a profile (when it's state changes). _callername_ is either **enter** or **exit** depending on whether the profile activated or deactivated. _subcallername_ is the name of the profile, if it has one, otherwise **anon**
    *   **scene**  
        a scene event, with _callername_ being the scene name. For element events, _subcallername_ is the element name. For action bar button presses, _subcallername_ is the label if one was given. For scene-global events (e.g. Key), _subcallername_ is event type
    *   **ui**  
        the Play button in the task edit screen in the Tasker UI
    *   **launch**  
        clicking a child application icon in the launcher
    *   **nbutton**  
        a notification action button, either from Tasker's permanent notification or one created with one of the Notify actions. _callername_ specifies the label of the button if present.
    *   **external**  
        an external application
    *   **qstile**  
        a Quick Settings tile. _callername_ specifies the label of the tile.
    *   **appshort**  
        an app shortcut (accessed via long-click on the Tasker icon). _callername_ specifies the label of the tile.
    *   **task**  
        another task, from a Perform Task action. _subcallername_ is the task name, if it has one, otherwise **anon**

##### Global Built-In Variables

*   **Airplane Mode Status**  
    `(dynamic)`  
    _%AIR_  
    Whether Airplane Mode is **on** or **off**
*   **Airplane Radios**  
    _%AIRR_  
    A comma-separated list of the radios which will be **disabled** when entering Airplane Mode.  
    Common radio names are: _bluetooth, cell, nfc, wifi, wimax_.
*   **Battery Level**  
    _%BATT_  
    Current device battery level from 0-100.
*   **Bluetooth Status** `(dynamic)`  
    _%BLUE_  
    Whether Bluetooth is **on** or in some other state (**off**).  
    
*   **Calendar List**  
    _%CALS_  
    Newline-separated list of calendars available on the device.  
    Each entry is in the format _calendarprovider:calendarname_.  
    Example usage:
    
    	Variable Set, %newline, \\n
    	Variable Split, %CALS, %newline
    	Flash, %CALS(#) calendars, first one is %CALS(1)
    
    For the sign _\\n_, press carriage-return on the keyboard.
*   **Calendar Event Title / Descr / Location** _%CALTITLE / %CALDESCR / %CALLOC_  
    The title, description and location of the **current** calendar event, if there is one. If there are multiple current calendar events the variables refer to the **shortest**.  
    Tip: find other details about the current event(s) using the `Misc / Test` action, specifying %TIMES for the data.
*   **Call Name / Number/ Date / Time (In)** `(dynamic, monitored)`  
    _%CNAME / %CNUM / %CDATE / %CTIME_  
    The caller name, number, date and time of the current (if a call is in progress) or last call received.  
    Caller number is **0** if it's unknown.  
    Caller name is **?** if it's unknown (probably because the caller number was blocked) and set to the caller number if the contact couldn't be looked up. It's unavailable on Android versions prior to 2.0.
*   **Call Name / Number/ Date / Time / Duration (Out)**`(dynamic, monitored)`  
    _%CONAME / %CONUM / %CODATE / %COTIME / %CODUR_  
    The called name, number, date and time of the last (**not** the current) outgoing call made.  
    Called Name is set to the called number if the contact couldn't be looked up. It's unavailable on Android versions prior to 2.0.
*   **Cell ID** `(dynamic,monitored)`  
    _%CELLID_  
    The current cell tower ID if known.  
    If you are using a Cell Near state, note that sometimes the Cell Near state will stay active even though %CELLID reports that the tower ID is unknown or invalid; that is because Cell Near only responds to valid IDs to prevent the state becoming inactive e.g. due to a service interruption.  
    For backwards compatibility, UMTS cells are reported with a GSM prefix.  
    From Android 4.2, Tasker version 4.3+, cells could be found from 2 different network types simultaneously. In that case, the value is reported with preference for the network type leftmost on the list: GSM, CDMA, UMTS, LTE.
*   **Cell Signal Strength** `(dynamic,monitored)`  
    _%CELLSIG_  
    The current phone signal level from 0-8 inclusive on a rougly linear scale. On some phones, the level will rise in steps of 2 (0,2,4,6,8). The value is -1 if the value is unknown or there is e.g. no service.  
    From Android 4.2, Tasker version 4.3+, cells could be found from 2 different network types simultaneously. In that case, the value is reported with preference for the network type leftmost on the list: GSM, CDMA, UMTS, LTE.  
    There is a bug with some Android versions that the reported signal strength is not updated until the device is turned off and on.
*   **Cell Service State** `(dynamic,monitored)`  
    _%CELLSRV_  
    The current phone service state. One of _unknown, service, noservice, emergency, nopower_.
*   **Clipboard Contents**  
    `(dynamic,monitored)` _%CLIP_  
    The current contents of the system clipboard.
*   **CPU Frequency**  
    _%CPUFREQ_  
    The current frequency CPU 0 is running at. See also: [CPU Control](#cpu.html).
*   **CPU Governor**  
    _%CPUGOV_  
    The current governor controlling the frequency of CPU 0. See also: [CPU Control](#cpu.html).
*   **Date**  
    _%DATE_  
    Current human-readable date.
*   **Day of the Month**  
    _%DAYM_  
    Current Day of the Month, starting at 1.
*   **Day of the Week**  
    _%DAYW_  
    Current Day of the Week starting with Sunday.
*   **Device ID / Manufacturer / Model / Product**  
    _%DEVID / %DEVMAN / %DEVMOD / %DEVPROD_  
    The ID, manufacturer, model and product name of the device.  
    Note: ID is **not** a unique identifier for the device, but rather for the hardware of the device. See also: %DEVTID.
*   **Device Telephony ID**  
    _%DEVTID_  
    Returns the unique telephony-based ID for the device (e.g. for GSM the IMEI, for CDMA the MEID or ESN).  
    Not available on all devices.
*   **Display Brightness** _%BRIGHT_  
    Current screen brightness, 0-255. On some devices, if the Android setting Auto Brightness is enabled, the value will always be 255.
*   **Display Timeout** _%DTOUT_  
    Current system screen timeout (seconds).
*   **Email From / Cc / Subject / Date / Time** `(dynamic)`  
    _%EFROM / %ECC / %ESUBJ / %EDATE / %ETIME_  
    The From, Cc, Subject, Received Date and Received Time of the last email received by the K9 email agent.
*   **Free Memory**  
    _%MEMF_  
    System free memory remaining in MB.
*   **GPS Status**  
    (monitored,dynamic Gingerbread+) _%GPS_  
    Whether the system GPS receiver is **on** or **off**.
*   **Heart Rate** `(monitored,dynamic)`  
    _%HEART_  
    The current detected heart rate in beats per minute.  
    See also: state _Heart Rate_.  
    The value will be negative for no contact (-1), accuracy unreliable (-2) or some other problem (-3)
*   **HTTP Response Code / Data / Content Length**  
    `(dynamic)`) _%HTTPR / %HTTPD / %HTTPL_  
    Values from the last HTTP POST/GET action.  
    If the server doesn't return a content length, %HTTPL will be calculated from the returned data where possible.
*   **Input Method**  
    _%IMETHOD_  
    The current active input method. Consists of 4 parts separated by commas: Method Name, SubType Name, Mode, Locale.  
    To access particular parts, use the _Variable Split_ action.
*   **Interrupt Mode** `(dynamic)`  
    _%INTERRUPT_  
    Only available on Android 5.0+, **requires Tasker's notification access service to be enabled**, see Android's Sound & Notification settings.  
      
    Android 5.0+: the current state of interruptions mode on the device: **none**, **priority** or **all**  
    See Also: action _Interrupt Mode_  
      
    Android 6.0+: the current state of Do Not Disturb mode on the device: **none**, **priority**, **all** or **alarms**  
    See Also: action _Do Not Disturb_
*   **Keyguard Status**  
    _%KEYG_  
    Whether the Keyguard is **on** or **off**
*   **Last Application**  
    _%LAPP_  
    The name of the application that was in the foreground before the current one e.g. Maps.
*   **Last Photo**  
    _%FOTO_  
    The filesystem path to the last photo taken by Tasker or the standard system camera application.
*   **Light Level** `(dynamic,monitored)`  
    _%LIGHT_  
    The last recorded light level in lux.  
    Note that Android does not return a value until the light level changes, so to test the sensor is working you should put it near a bright light initially.  
    May not change when the device display is off, see `Menu / Prefs / More / Display Off Monitoring / Light Sensor`.
*   **Location** `(dynamic)`  
    _%LOC_  
    The latitude and longitude of the last GPS fix.  
    [See note](#locnote).
*   **Location Accuracy** `(dynamic)`  
    _%LOCACC_  
    The accuracy in metres of the last GPS fix.  
    [See note](#locnote).
*   **Location Altitude** `(dynamic)`  
    _%LOCALT_  
    The altitude in metres of the last GPS fix, or 0 if unavailable.  
    [See note](#locnote).
*   **Location Speed** `(dynamic)`  
    _%LOCSPD_  
    The speed in metres/second at the last GPS position fix or 0 if unavailable.  
    [See note](#locnote).
*   **Location Fix Time Seconds** `(dynamic)`  
    _%LOCTMS_  
    The time in seconds of the last GPS fix. To get age of fix, take this away from %TIMES.  
    This value is not set until an offset of the GPS time from the fixed time has been calculated (should be after the first GPS fix) because the value is meaningless until that point.  
    [See note](#locnote).
*   **Location (Net)** `(dynamic)`  
    _%LOCN_  
    The latitude and longitude of the last network location fix.  
    [See note](#locnote).
*   **Location Accuracy (Net)** `(dynamic)`  
    _%LOCNACC_  
    The accuracy in metres of the last network location fix.  
    [See note](#locnote).
*   **Location Fix Time (Net)** `(dynamic)`  
    _%LOCNTMS_  
    The time in seconds of the last net location fix. To get age of fix, take this away from %TIMES.  
    [See note](#locnote).
*   **Magnetic Field Strength** `(monitored,dynamic)`  
    _%MFIELD_  
    The total magnitudes in micro-Teslas of the magnetic fields acting on all three axis of the devices sensor.  
    Updated once per second.  
    See Also: state `Magnetic Field`.
*   **Music Track** `(dynamic,monitored))`)  
    _%MTRACK_  
    The current playing music track, supported for:
    
    *   Tasker actions _Music Play_ and _Music Play Dir_
    *   Built-in Android music-player, probably not on all devices however
    *   Power AMP
    *   BeyondPod (Tasker v1.2.1+)
    *   Phantom Music Control Pro
    *   Media Utilities
    
    Priority: if both Tasker and one of the other supported apps are playing simultaneously, the non-Tasker track will be shown. If more than one of the other supported apps is playing simultaneuosly, behaviour is unspecified.  
    Notes:
    *   if you don't have a supported player, you could try Phantom Music Control Pro or Media Utilities, which support a lot of players and should pass the info on to Tasker
    *   pausing a track clears the variable, unpausing sets it again
    *   your music player may need an option enabled in order to broadcast the track information, or the broadcast may only be available in a 'pro' version
*   **Muted**  
    _%MUTED_  
    Whether the microphone is currently muted (**on**) or not (**off**).
*   **Night Mode**  
    _%NIGHT_  
    The current Android Night Mode.  
    One of **on**, **off** or **auto**.  
    If **auto**, Android will decide whether it should be in Night Mode itself.
*   **Notification Title** `(monitored, dynamic)`  
    _%NTITLE_  
    The title of the last notification shown in the status bar. Prior to KitKat, requires Tasker's accessibility server to be running (see Android Accessibility Settings). From KitKat, requires Tasker's Notification Listener service to be running instead.  
    In a task running as a result of a `Notification` or `Notification Removed` event, use variable %evtprm2 instead of %NTITLE. This is much more reliable and you have access to other parts of the notification (%evtprm3 etc)  
    Notifications generated by Tasker are not shown.
*   **Phone Number**  
    _%PNUM_  
    The current phone number of the device, if it's in service.  
    On some phones it doesn't work (Android limitation), seems related to the type of SIM.
*   **Pressure** `(monitored,dynamic)`  
    _%PRESSURE_  
    The current air pressure on the device in millibars.  
    May not change when the device display is off, see `Menu / Prefs / Monitor / Display Off Monitoring / Pressure Sensor`.
*   **Profiles Active** `(dynamic)`  
    _%PACTIVE_  
    A comma-separated list of the currently active, named profiles in activation order. Duplicate names will appear on the list only once. The list always starts and ends with a comma to make matching easier, if it's not empty.
*   **Profiles Enabled** `(dynamic)`  
    _%PENABLED_  
    A comma-separated list of the currently enabled, named profiles in creation order. Duplicate names will appear on the list only once. The list always starts and ends with a comma to make matching easier, if it's not empty.
*   **Roaming**  
    _%ROAM_  
    **on** if device is roaming on the current telephone network, otherwise **off**.
*   **Root Available**  
    _%ROOT_  
    **yes** if root functions are available on this device, otherwise **no**.
*   **Screen** `(dynamic)`  
    _%SCREEN_  
    Whether the screen is on (value **on**) or off (value **off**).
*   **SDK Version**  
    _%SDK_  
    The numeric Android [SDK version](http://developer.android.com/reference/android/os/Build.VERSION_CODES.html) of the device.
*   **Silent Mode** `(dynamic)`  
    _%SILENT_  
    The current state of silent mode: **off**, **vibrate** or **on**.  
    From Android 5.0+ this variable is intended to only reflect whether the device is in vibrate mode (**vibrate**) or not (any other value), but the **on** value is included for backwards compatibility and set when the device is not in vibrate mode and the interrupt mode is **none** or **priority**.  
    See Also: variable _%INTERRUPT_, actions _Silent Mode_ and _Interrupt Mode_.
*   **SIM Serial Number**  
    _%SIMNUM_  
    The serial number of the SIM card, if one is present and accessible.  
    If the SIM has not been unlocked it will not be available.
*   **SIM State**  
    _%SIMSTATE_  
    The current state of the SIM card.  
    One of **unknown**, **absent**, **pinrequired**, **pukrequired**, **netlocked** or **ready**.
*   **Speakerphone**  
    _%SPHONE_  
    Whether the speakerphone is **on** or **off**
*   **Speech** `(dynamic)`  
    _%SPEECH_  
    The current utterance as a result of a _Say_ or _Say File_ action, if applicable.
*   **Tasks Running** `(dynamic)`  
    _%TRUN_  
    A comma-separated list of any named tasks which are currently running. The list always starts and ends with a comma to make matching easier, if it's not empty.
*   **Telephone Network** `(dynamic, monitored)`  
    _%TNET_  
    The current telephony network operator the device is using.  
    May be unreliable on CDMA networks
*   **Temperature** `(monitored,dynamic)`  
    _%TEMP_  
    The current ambient temperature in degrees Celsius.  
    May not change when the device display is off, see `Menu / Prefs / Monitor / Display Off Monitoring / Temp. Sensor`.  
    See also: state _Temperature_.
*   **Text From/Date/Subject/Time** `(monitored)`  
    _%SMSRF / %SMSRN / %SMSRB / %MMSRS / %SMSRD / %SMSRT_  
    The sender address, name, body, subject, date and time of the last text (SMS or MMS) received.  
    These variables will be empty until the first time a text is received after they have been referenced because Tasker does not monitor texts unless it's needed.  
    _Name_ is set to sender address of no contact could be looked up. It's unavailable on Android versions prior to 2.0.  
    _Body_ (%SMSRB) is only set for SMSs.  
    _Subject_ (%MMSRS) is only set for MMSs.
*   **Time**  
    _%TIME_  
    Current human-readable time separated by a period e.g. 10.59
*   **Tether** (dynamic)  
    _%TETHER_  
    A comma-separated list of enabled tethering forms i.e. connections over which another device can connect to this one in order to use its internet connection.  
    The possible forms are **wifi**, **usb** or **bt**.  
    BT will only be present when an actual client is connected via BT for using the devices network connection, whereas the others will be present as soon as the functionality is enabled (Android bug/limitation).
*   **Time MilliSeconds**  
    _%TIMEMS_  
    The current time in milliseconds.  
    (milliseconds since some time in January, 1970, if you must know).
*   **Time Seconds**  
    _%TIMES_  
    The current time in seconds.  
    (seconds since some time in January, 1970, if you must know).
*   **UI Mode** `(dynamic,monitored)`  
    _%UIMODE_  
    The current Android UI mode.  
    One of **car**, **desk**, **appliance**, **tv** (television), **watch**, **undef** (undefined) or **normal**.
*   **Uptime Seconds**  
    _%UPS_  
    The number of seconds since the device last booted.
*   **Volume - Alarm/Call/DTMF/Media/Notification/Ringer/System** `(dynamic)`  
    _%VOLA / %VOLC / %VOLD / %VOLM / %VOLN / %VOLR / %VOLS_  
    Current audio channel volume level.  
    On some devices, volume changes are not picked up dynamically, on others not when using the phone app.
*   **WiFi Info**  
    _%WIFII_  
    When connected to an Access Point (AP), shows human-readable data about the AP. When not connected, show details of the most recent Wifi scan results for nearby APs.
*   **WiFi Status** `(dynamic)`  
    _%WIFI_  
    Whether WiFi is **on** or **off**. Note: if WiFi is enabling or disabled, in fact anything but enabled, it's classed as off.
*   **Wimax Status**  
    _%WIMAX_  
    Whether Wimax is **on** or **off**. Note: if Wimax is enabling or disabled, in fact anything but enabled, it's classed as off.
*   **Window Label** `(monitored)`  
    _%WIN_  
    The label of the current window, which could be a full-screen activity or a dialog.  
    Not set if the label is unknown.  
    For some windows, the label might be that of the first item in the window e.g. a menu entry or even a button.

##### General Notes

Variables marked `dynamic` in the list above trigger changes in _Variable Value_ states and _Variable Set_ events whenever their value changes.

Variables marked `monitored` will cause the relevant monitor to startup to track their state when they are used in contexts or tasks which are used by widgets or **enabled** profiles. For instance, %CELLID used in a Flash action will cause cell location to be tracked.

Limitation: monitored variables cannot be detected in anonymous shortcuts.

##### Note On Location Variables

When the relevant provider (Net or GPS) of a location context is active, these variables report the values from the provider, which may be more recent than Tasker has seen if other applications are asking for location.

When the relevant provider is **not** active, these variables report the last values **seen by Tasker**, which could be the result of a `Get Location` action or of monitoring for a `Location Context`.

That means the the reported fix times could **go backwards**, if you turn off the location provider between two uses of the variables.

Location variables can also be manually updated by running the `Get Location` action.

#### User Variables

The action _Variable Set_ (and several others) can be used to create new variables. Variable names have the following restrictions:

*   they must start with the **%** character
*   they are case-sensitive
*   then must at least a further **3** alphanumeric characters
*   they can also contain the underscore character (\_) but not start or end with it

In general, it's best to use local variables wherever possible because:

*   you know they won't be interfered with by other tasks or scenes
*   they are more efficient in several ways

Note: multiple copies of the same task running at the same time each have their own separate copy of their local variables.

###### Scene-Local Variables

Each scene has its own set of local variables which it shares with the task that created it; both the scene and task see changes to the variables made by either.

Any task which starts as a result of a scene event (e.g. a tap on an element) also shares the variables of the scene (and thus of the original task which created the scene).

As a consequence, a task started by a scene event (e.g. Tap on an element) which shows a new scene e.g. via the _Show Scene_ action, will result in the second scene sharing the variables of the first scene.

When a task shows a scene that was created by a different task (or a different copy of the same task) and subsequently hidden, the task's variables are **copied** to the scene variables (overriding values of variables which already exist) but the task does **not share** the scene variables and cannot see changes to them.

##### Escaping Variable Names

If you want to prevent a variable name being replaced, put a **\\** in front of it e.g.

> `Variable Set, %new, \%old`

Will set the value of _%new_ to _%old_, **not** the **value** of _%old_.

In order to precede a variable name with a **\\** you can escape the backslash e.g.

> `Variable Set, %new, \\%old`

Will set the value of _%new_ to **\\** followed by the **value** of _%old_.

##### Variable References

It's possible to indirectly refer to variables by preceeding one or more extra **%** signs to the start of the variable name. For example:

> `Variable Set, %colour, red   Variable Set, %varname, colour   Flash %%varname`

... will flash **red**.

Using this notation it's possible to assign variables whose name is not known beforehand:

> `Read File, variablename.txt, To Var, %varname   Variable Set, %%varname, red`

This will set the variable whose name is stored in the file `variablename.txt` to **red**.

You can nest references as deeply as you like (e.g. `%%%%var`) but mental stress and bugs are sure to follow.

If any part of the chain has an invalid variable name then the original reference will be returned. In the first example, if `%varname` is set to `!!!`, then **%%varname** will be flashed instead of **red**.

##### Variable Lifetime

The value a **global** variable holds lasts until Tasker is uninstalled if it is not changed by any task.

**Local** variables are lost at the end of the task they were created in, or when the parent scene is destroyed in the case of tasks called from scenes.

##### Uninitialized Variables

User-variables which have not had a value assigned do not have replacements carried out e.g. in the expression _I love %fruit_, if %fruit is uninitialized, the expression remains as it is, otherwise %fruit is replaced with the value.

Exception: uninitialized variables used in mathematical expressions are replaced with 0.

#### Variables In Plugins

Plugin developers can tell Tasker to replace variables it finds in plugin strings with their current Tasker value. If you have a plugin which doesn't support this, send the developer this URL

> [http://tasker.dinglisch.net/plugins.html](http://tasker.dinglisch.net/plugins.html)

which has the relevant details.

#### Variable Arrays

Tasker supports pseudo-arrays.

They are especially useful when used with the `For` action, since you can perform a set of actions on each element in turn e.g. list a set of files then test each one.

##### Examples

If the four variables **%arr1, %arr2, %arr3, %arr4** hold respectively **a, b, c** and **d** then we have an array with 4 _elements_. These variables can be used just like any other, however it is also possible to access them in special ways. Here are some examples:

*   **%arr(#)**  
    The number of defined array elements (**4** in this case)
*   **%arr(#>)**  
    The index of the first defined array element, or **0** if none are defined (**1**).
*   **%arr(#<)**  
    The index of the last defined array element, or **0** if none are defined (**4**)
*   **%arr(#?b/c)**  
    A comma-separated list of the array indices (lowest to highest) with matching values, or **0** if none match (**2,3** in the example)
*   **%arr(>)**  
    The contents of the first defined array element (**a**)
*   **%arr(<)**  
    The contents of the last defined array element (**d**)
*   **%arr()** or **%arr(:)**  
    All of the array elements separated by commas (**a,b,c,d**)
*   **%arr(2)** or just **%arr2**  
    The content of the element with index 2 (**b**)
*   **%arr(2:4)**  
    Contents of defined elements with indices 2 to 4 (**b,c,d**)
*   **%arr(:3)**  
    All the defined elements with indices up to 3 (**a,b,c**)
*   **%arr(3:)**  
    All the defined elements with indices starting from 3 (**c,d**)
*   **%arr(1:2)**  
    All the defined elements with indices from 1 to 2 (**a,b**)

Notes:

*   arrays will virtually always have all their elements defined so e.g. %arr(>) will be the same as %arr(1), %arr(#) will be the same as %arr(#<)
*   index specifiers can themselves be variables (e.g. %arr(1:%MAX) or %arr(#?%FINDME)) but **not** variable arrays

##### Creating An Array

1.  using `Array Set`:  
    **Array Set, %arr, a b c d**
2.  using `Variable Split` on an existing (simple) variable:  
    **Variable Set %arr a b c d**  
    **Variable Split %arr**  

3.  by assigning individual elements with `Variable Set`:  
    **Variable Set, %arr3, c**.
4.  using `Array Push` to add an initial element
5.  some other actions also create arrays for their results e.g. `List Files`.

##### Inserting Elements

Use the `Array Push` action.

The _Fill Spaces_ parameter might need more explanation. It is only relevant if one or more of the array elements are undefined. As an example, if we have the array elements %arr1 and %arr3 containing **apple** and **banana**:

*   **Array Push %arr1, 1, pear**  
    leaves %arr1, %arr2 and %arr4 containing **pear**, **apple** and **banana**.  

*   but **Array Push %arr2, 1, pear, Fill Spaces**  
    leaves %arr1, %arr2 and %arr3 containing **pear**, **apple** and **banana**.

##### Removing Elements

Use the `Array Pop` action. Note the difference between `Array Pop` and `Variable Clear`: `Pop` reduces the number of elements in the array, while `Clear` merely changes elements to undefined.

Example: if we have the array elements %arr1, %arr2, %arr3 containing **apple**,**pear** and **banana**:

*   **Variable Clear %arr2**  
    leaves %arr1 and %arr3 containing **apple** and **banana**.  
    
*   but **Array Pop %arr2**  
    leaves %arr1 and %arr2 containing **apple** and **banana**.

##### Deleting An Array

Use `Array Clear`.

In most cases you could also use **Variable Clear %arr\*** with Pattern Matching checked, but that would also delete variables called e.g. %arrTOODEETOO so `Array Clear` is safer.

##### Sorting

The `Array Process` action offers various sorting options, amongst other things.

##### Array Efficiency

Arrays are intended for convenience when processing high-level data, not for e.g. processing astronomical data. Doing thousands of array actions will likely take several seconds (although mostly due to the housekeeping work done by Tasker in-between each action rather than due to the array operations themselves).

In terms of storage efficiency, they are also fairly hopeless. You probably do not want to store tens of thousands of items in an array.
