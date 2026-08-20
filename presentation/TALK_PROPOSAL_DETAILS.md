
------

This is a proposal for a Python-focused talk about extending Jupyter with a custom kernel. Forth is used only as the case-study language.

### Talk Title

**Building a Jupyter Kernel for a Non-Python Language**

### Short talk description

<!-- 

Brief abstract about your talk (50-150 words). This will be used for our social media. 

Describe what your talk covers, who would benefit from it, and what key takeaways
attendees can expect. This description will be used for promoting your event on social media.

-->

Jupyter notebooks are not limited to Python. 
In this talk, we will build a practical mental model for a custom Jupyter kernel: register the kernel, in the kernel run code, send printed output and expression result to Jupyter. 
Using IForth, a kernel for the Forth language, we will follow one cell from the notebook frontend to a running GForth interpreter subprocess and back. 
Attendees will learn how to implement a custom Jupyter kernel in Python, and write automated tests for it using `jupyter_kernel_test`.

### Longer talk description

<!--

Describe what your talk covers, who would benefit from it, and what key takeaways
attendees can expect. This description will be used for promoting your event on social media.

Add a longer description of your talk: similar to the previous one, but with more details.

-->

What does a Jupyter notebook actually need from a kernel? 
A kernel process must be discoverable by Jupyter, receive an execution request, run code, publish output and return a valid reply. 
The Jupyter Notebook / Lab frontend and the kernel can be written in different languages and do not need to share memory.

We will explain custom kernel implementation using case study of IForth (a kernel for Forth language). 
IForth subclasses Jupyter's `Kernel` base class and implements execution in `do_execute`. 
We will trace how:

* a kernelspec lets Jupyter discover and launch the kernel
* stdout and stderr become `stream` messages
* code output becomes an `execute_result` 
  
We will also examine simple automated tests for the kernel using `unittest` and `jupyter_kernel_test`.

### What format do you have in mind?

20-minute talk followed by 10-minute Q&A.

### Talk outline / Agenda

<!--

Please provide a brief outline of your talk's structure.

Example:
• Introduction to the problem (5 mins)
• Core concepts and theory (10 mins)
• Live demo/code walkthrough (15 mins)
• Best practices and pitfalls (10 mins)
• Q&A (10 mins)

You may update this outline later as you prepare your talk.

-->

* Notebook demo (using IForth kernel) and a brief Forth vocabulary primer (3 minutes)
* The kernel implementation and Jupyter message flow (4 minutes)
* Building the kernel: `Kernel`, `do_execute` and kernelspec (7 minutes)
* Simple Automated Tests for the kernel
* Q&A (10 minutes)

### Key takeaways

<!--

What will attendees learn or gain from your talk?

Please 3-5 key takeaways that attendees can expect from your talk. Here are some rubrics:
• Understanding of [concept/technology/approach]
• Practical knowledge of [specific skill/technique]
• Best practices for [relevant area]
• Common pitfalls to avoid when [doing something]
• Resources and next steps for further learning

-->

* Understand how the Jupyter frontend, server and kernel process fit together.
* Implementation: A kernel process must be discoverable by Jupyter, receive an execution request, run code, publish output and return a valid reply. 
* Connect a kernel to a language interpreter via `subprocess`.
* Distinguish stdout, stderr, and expression results in Jupyter messages.

### What domain would you say your talk falls under?

**Python, Jupyter, and Developer Tooling**

The talk focuses on extending Jupyter from Python using `ipykernel` and writing automated tests for the kernel using `jupyter_kernel_test`.
Forth is used only as the case-study language - no prior knowledge of Forth is required.

### Duration (including Q&A)

30 minutes total: 20 minutes for the talk and 10 minutes for Q&A.

### Prerequisites and preparation

<!--

What should attendees know or prepare beforehand?

For example:
• Basic Python knowledge (functions, classes)
• Laptop with Python 3.8+ installed
• Familiarity with command line basics
• No prior experience with [specific technology] needed

We usually have a diverse audience, so please keep in mind that not everyone may be familiar with advanced topics.
If your talk requires specific tools or libraries, please mention them here.
If you plan to do a live demo, please ensure you have tested it on the event setup beforehand.
If you feel you will need help with this, please let us know.

-->

Basic Python knowledge and familiarity with running commands in a terminal are helpful. No prior Forth, Jupyter protocol, or kernel implementation experience is required. The live demo uses Python, Jupyter, and GForth in a prepared environment; attendees do not need to install anything.

### Resources and references

<!--

Any helpful resources for reviewers and attendees

• Links to relevant documentation
• GitHub repositories
• Articles or papers
• Tools or libraries used

-->

* IForth repository: https://github.com/sohang3112/iforth
* Jupyter kernels documentation: https://docs.jupyter.org/en/latest/projects/kernels.html
* Jupyter messaging protocol: https://jupyter-client.readthedocs.io/en/latest/messaging.html
* IPython kernel base class: https://ipykernel.readthedocs.io/en/stable/api/ipykernel.html
* Jupyter kernel testing: https://github.com/jupyter/jupyter_kernel_test
* GForth: https://gforth.org/

### Speaker bio

<!--

Tell us about yourself! This will be used for speaker introductions and promotional materials.

Include:
• Your background and current role
• Relevant experience with the talk topic
• Previous speaking experience (if any)
• Fun fact or personal interest
• How to reach you (email, social media)

Don't worry if you're a first-time speaker – we welcome everyone!

-->

I am a Software Engineer at HCLTech and am pursuing an MTech in AI at IIT Madras. I have used Python professionally for 4.5 years.

I maintain IForth, an open-source Jupyter kernel for the Forth programming language. Maintaining the project has given me hands-on experience with Jupyter kernels, Python subprocess management, asynchronous I/O, packaging, and integration testing. I am a first-time conference speaker.

Contact: sohangchopra@gmail.com | https://www.reddit.com/user/sohang-3112/

### Accessibility & special requirements

<!--

Are there any accessibility needs or special technical requirements for your talk?

For example:
• Screen reader compatibility is needed
• Large font requirements

-->

No special technical requirements. I will use a light background, high-contrast text, readable fonts, text-based code, and verbal descriptions of diagrams and output. I will bring a static fallback for the live demo.

### Additional comments

<!--

Anything else you'd like us to know?

• Are you a first-time speaker? We're here to help!
• Do you need mentorship or feedback on your talk?
• Special circumstances or considerations besides the ones stated above?
• Do you have any other questions about the process that do not fit the requests stated above?
• Did you find an issue with this questionnaire or have suggestions to improve it? Please let us know here or [open a separate issue](https://github.com/pydelhi/talks/issues/new?template=BLANK_ISSUE), and we will be happy to hear from you!

-->

I am a first-time speaker and would welcome feedback on the framing, accessibility, and timing of the talk. I will provide draft slides and demo materials for review.






