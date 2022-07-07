+++
author = "Toni Sagrista Selles"
categories = ["Libgdx"]
tags = ["libgdx" , "programming", "java" ]
date = "2013-07-05"
description = "A migration story"
linktitle = ""
title = "From Slick to Libgdx"
type = "post"
+++

A couple of posts ago I mentioned I would write a few lines about my experience with the **migration of my [RTS engine](/blog/2013/rts-engine-preview) from [Slick](https://slick.ninjacave.com/) to [Libgdx](https://libgdx.com/)** and that's what I'll do in this post. I'll be talking very lightly on some issues such as the code structure, the rendering process, the camera, etc. **If you need a starting tutorial please refer to the official documentation**, this is not what you are looking for. I'm just trying to give my impressions in the migration process I had to undertake. But first I want to back up a little and give a **quick overview of both libraries**.

<!--more-->

## Library overview
-   On the one hand, **Slick** is a high-level 2D java gaming library originally created and maintained by Kev from cokeandcode.com. I have used it in the past for some projects and it really is **very easy and straightforward** to use, with a well designed API and tons of documentation. It adds a layer on top of [LWJGL](https://lwjgl.org), a Java binding for OpenGL 1.x, OpenAL and OpenCL, allowing for rookie and experienced programmers alike to write 2D game-like applications without having to mess with lower level libraries, specially OpenGL. Slick offers support for images, animations, particles, sounds, music, Tiled tile maps, Phys2D and much more. I'd say its strongest asset is that it keeps things simple, being it also its doom as it may not be as appealing to more advanced users. In addition, the project seems rather dying now since Kev stopped maintaining it and handed it over to someone.
-   On the other hand, **Libgdx** is an advanced java gaming library with support for cutting-edge technologies and platforms. It really is a vast improvement over Slick if you want to create really modern and graphically rich games. It offers most, if not all, the features Slick does, and also works with [LWJGL](https://lwjgl.org) underneath. Libgdx has tons of tools and utilities that make your development easier such as a texture packer, a project setup UI and a particle editor. It does a bunch of complicated stuff for you such as sprite batching, texture atlas management, session handling in Android and much [more](https://libgdx.com/features). Libgdx's cross platformness (I like inventing words...) extend from Windows, Mac and Linux to Android, iOS and HTML5, making it very useful to code your app once and run it everywhere. Overall, Libgdx is a more advanced library, it has a very active community and I would strongly recommend its use to anyone starting. If you just want to write a 2D game and keep things simple, you can always use [mini2Dx](https://mini2dx.org/), an easy-to-use 2D API built on top of Libgdx.

## Migration

Ok, so **why did I choose to migrate** from one to the other? Well, I think the question answers itself if you look at my overview of both projects. Additionally, I use to work on my little applications from time to time and several months may pass from when last worked on them until I take it over again. Last time this happened, I found slick not maintained anymore by its original creator and the page set up by the new maintainers was having issues. That's when I started looking for alternatives and ran into Libgdx. It looked very attractive and seemed the project was actively supported, so I gave it a go. I couldn't be happier with the choice, I must add. Let's get started with the migration then.

### Code structure

Slick does not differ from a classic Java project. You just put your libraries in the lib folder and you are ready to go. **Libgdx** is a different matter. You have the core project where all your code and dependencies are put, let's call it *MyProject*. This contains your "game" class. Then, you need an Android project called *MyProject-android* where you need to put all the project's resources such as images and maps, and all the Android specific files like the `AndroidManifest.xml`. That's all you need if you want your application to run in Android. Additionally, you need extra optional projects if you want the desktop and HTML5 versions. Each platform-specific project has at least a main class which creates an instance of the "game" class. For instance, in the Android project you'd have an `Activity` with an `onCreate()` method like this:

{{< highlight java "linenos=table" >}}
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        AndroidApplicationConfiguration cfg = new AndroidApplicationConfiguration();
        cfg.useGL20 = false;
        initialize(new MyGame(), cfg);
    }
{{< /highlight >}}

In desktop, you'd have a main class creating an instance of `LwjglApplication` passing `MyGame` as a parameter. There's a pretty good description of the project [here](https://code.google.com/p/libgdx/wiki/ProjectSetup).

The good news is that all this can be set up automatically and also updated to the latest Libgdx version using their setup tool. Clean and easy! More info [here](https://code.google.com/p/libgdx/wiki/ProjectSetupNew).

### Main loop

The first thing you'll notice is that Libgdx does not manage the main loop for you providing `update()` and `render()` methods like Slick does, so it is up to the programmer to implement this. However, what Libgdx does provide is a `render()` function defined in the `ApplicationListener` interface which is called every time rendering should be performed, so we need to both update and render our entities in this method. Slick provided an update(`GameContainer` container, int delta) method which received the delta time in ms. Now, we can get the delta time since the last `render()` call using `Gdx.graphics.getDeltaTime()`, so no hassle here.

### Drawing sprites and shapes

In **Slick** the drawing process is very simple, for the `Sprite` class itself has different draw methods. To draw shapes a class called `ShapeRenderer` is used in the following fashion:

```java
ShapeRenderer.draw(new Line(pos.x, pos.y, pos.x + vel.x, pos.y + vel.y));
```

In **Libgdx** sprites and shapes are batched and the whole process is a bit more low-level, but you have more control over everything. Now you need to start the sprite batch before drawing and end it after:

{{< highlight java "linenos=table" >}}
batch.setProjectionMatrix(camera.combined);
batch.begin();
batch.draw(spriteImage, position.x, position.y);
batch.end();
{{< /highlight >}}

You may have noticed the `setProjectionMatrix(Camera camera)` chunk. This is because Libgdx offers cameras pretty much in the same fashion as OpenGL does. This line just tells the batch the position of the drawn sprites must be determined by the camera's position.

The rendering of basic shapes in Libgdx is a bit trickier than in Slick:

{{< highlight java "linenos=table" >}}
shapeRenderer.begin(ShapeType.Filled);
shapeRenderer.setColor(new Color(0f, 0f, 1f, .4f));
shapeRenderer.rect(cell.bounds.x, cell.bounds.y, cell.bounds.width, cell.bounds.height);
shapeRenderer.end();
{{< /highlight >}}

You need to begin and end the `shapeRenderer` with either "filled" or "line", set the color and draw the shape. Remember to enable `BLENDING` and `SRC_ALPHA` if you want transparencies, and disable them at the end. Mix sprite drawing with shape rendering in the code is not a good idea, so keep them separated if you don't want to run into problems later.

### Tiled integration

The integration with Tiled is good in both projects but the API and the implementation is probably more accurate to the `TMX` format in Libgdx, where there are classes for tiled maps, tiled layers, object layers, each with its attributes. The best you can do is look at the API and figure it out yourself, for the details are numerous. There's a good starting point [here](https://code.google.com/p/libgdx-users/wiki/Tiles).

### Camera

Finally, we'll briefly talk about the camera. As long as I know Slick does not offer a Camera class, but Libgdx does. Libgdx offers an orthographic camera, with a parallel projection, suitable for 2D games, and a perspective camera which uses a perspective projection, suitable for 3D games. In my application with Slick I created a camera class which managed the position and movement of the camera. To convert it to Libgdx, I converted this camera class into a wrapper over the `OrtographicCamera` so that the interface stayed the same.

## Conclusions

It took me about a couple of days to migrate the whole thing but it is worth it. Now my application runs in Android and the performance has benefited from batching and texture mapping. I'd say that the rendering process of Libgdx is more difficult but it also offers more possibilities. If you want to keep things very simple, stick with Slick. If you don't mind having to spend a bit longer in the learning process, go for Libgdx, you won't regret it.
