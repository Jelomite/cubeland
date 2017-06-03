# Cube Land


*Cube Land* is a voxel based sculpting engine, for multiple users.
  - Join *Cube Land*
  - Create a sculpture
  - Magic

### Technologies involved

*Cube Land* uses a number of open source projects to work properly:

- openGL
- pygame
---
### Installation

*Cube Land* requires [python3.6](https://www.python.org/downloads/release/python-361/) to run.

Install the dependencies and devDependencies and start the server.

```sh
$ pip install pygame pyopengl
```

### Usage

###### Once you installed the dependencies, it's all fairly simple.

Starting the server:

```sh
$ cd cubeland
$ python server.py [PORT]
```

Launching the application:

```sh
$ python main.py [IP] [PORT]
```

---
## Demo:
##### how the application looks after few block placements.
![alt text](https://i.imgur.com/WCweq24.png "Cubeland structure in progress")

### Controls:

- **W** - walk **forward**
- **A** - walk **right**
- **S** - walk **backward**
- **D** - walk **right**
- **Shift** - descend
- **Space** - ascend
- **MOUSE1** - **place** block
- **MOUSE2** - **delete** block