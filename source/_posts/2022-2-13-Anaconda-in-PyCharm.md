---
title: Anaconda in PyCharm
date: 2022-02-13 22:55:55
categories:
- [知识科普]
- [学习笔记]
tags:
- PyCharm
- Anaconda
- Python
index_img: https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main/img/2022/others/jiaocha-2.jpg
banner_img: /img/default3.png
comment: 'valine'
excerpt: I get used to pip before, many people suggest me to try Anaconda, so let's try!
---

## What is Anaconda

Anaconda is a powerful package management tool, it solves some weakness when using python. For example, the inconvenience of switching among different versions of python interpreters and many site-packages. It is similar to the function of `pip` and `pip3`, but it is more powerful.

## Install Anaconda

Follow the instruction in 在 [Linux 上安装](https://anaconda.org.cn/anaconda/install/linux/), which supports chinese. First, you would be asked to download some dependence by the following code (my OS is Ubuntu20.04):

```bash
sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
```

Then you would get a `.sh` file, give it executable permission. Run the `.sh` file to install Anaconda just like in Windows. Press `Enter` all through the progress, you better install Anaconda in the default location, which is under the `/home/` directory. Mention that do not put it under `/usr`, the official site give a warning about this! 

```bash
chmod +x filename.sh
./Anaconda3-2021.11-Linux-x86_64.sh 
```

```bash
Anaconda3 will now be installed into this location:
/home/name/anaconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/home/name/anaconda3] >>> 
```

After that you would be asked to init the environment, which is actually adjusting the `.bashrc` file, like using `source <path to conda>/bin/activateconda init`. After all the steps, you would get a respond "Thank you for installing Anaconda3!"

## Anaconda-navigator

Anaconda-navigator is a GUI application provided by Anaconda, you could use it to manage virtual environments without using terminal. Switch to the "Environments" Tab, choose the env that you are interesting. There are 5 types of selections: *Installed, Not installed, Updatable, Selected, All*. If you want to install a new package, one method is to choose *Not installed*, and then search the package you want and download it.

## Config PyCharm

If you haven't got PyCharm, go to [this link](https://www.anaconda.com/pycharm) to download it! Then in the *New Project* page, choose Conda to manage the new environment.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/20220213232131.png" width="600"></center>

In the *Settings* Tab, you could add and remove packages.

<center><img src="https://cdn.jsdelivr.net/gh/Judera9/Pictures-for-Blogs@main//img/2022/others/20220213235222.png" width="600"></center>