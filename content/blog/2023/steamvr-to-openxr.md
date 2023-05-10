+++
author = "Toni Sagristà Sellés"
title = "OpenXR to the rescue"
description = "The tale of a migration from OpenVR to OpenXR"
date = "2023-05-09"
linktitle = ""
featured = ""
featuredpath = ""
featuredalt = ""
categories = ["Programming"]
tags = ["gaia sky", "graphics", "technical", "vr", "virtualreality", "openxr", "steamvr", "openvr", "english"]
type = "post"
draft = false
+++

[Gaia Sky](https://zah.uni-heidelberg.de/gaia/outreach/gaiasky) has been using the [OpenVR API](https://github.com/ValveSoftware/openvr) from SteamVR for the last few years to power its Virtual Reality mode. However, the API is notoriously poorly documented, and it only works with the SteamVR runtime.[^1] That leaves out most of the existing VR headsets. Luckily, the main vendors and the community at large joined efforts to come up with an API that would be adopted by all and backed by the Khronos Group: [OpenXR](https://www.khronos.org/openxr/). Obviously, since Gaia Sky is actively maintained, it is only natural that a migration to the newer and widely supported API would happen sooner or later. But such a migration is not for free. Both APIs are wildly different, with OpenXR being much more verbose and explicit. In this post, I document the migration process and also offer a bird's eye view of the layout, structure and components of an OpenXR application for Virtual Reality.

<!-- more -->

## Final Product

Yesterday I fixed the last app-breaking bug in the OpenXR port of Gaia Sky. Here is a post about it, with a nice video of Gaia Sky VR.

<iframe src="https://mastodon.social/@jumpinglangur/110339029481138017/embed" class="mastodon-embed" style="max-width: 100%; border: 0" width="100%" allowfullscreen="allowfullscreen"></iframe><script src="https://mastodon.social/embed.js" async="async"></script>

<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>

## Resources

OpenXR is a complex and verbose API, and much more difficult to 'pick up and write' than OpenVR, which abstracts a lot of the functionality and is direct and to the point. I have used several resources in my journey to a fully-functioning OpenXR build of Gaia Sky VR:

- **Official OpenXR documentation** --- OpenXR has amazing documentation which should be the starting point for everyone looking to use the API.[^2]
- **LWJGL3** --- Gaia Sky uses Java (for reasons), so bindings to the C OpenXR library are required. These are provided by the amazing LWJGL3 project, along with the base framework, and the bindings to other APIs like OpenGL and GLFW.[^3]
- **MCXR** --- a VR Minecraft mod using OpenXR.[^4]


## OpenVR

I initially implemented the VR version of Gaia Sky back in 2018 after we acquired an Oculus Rift CV1 headset for tests. Back then there were essentially two serious consumer headsets: The Oculus Rift CV1 (released after the development kits 1 and 2), and the HTC Vive. There were also two competing APIs: **OpenVR**, pushed by SteamVR, and supported natively by the Vive natively and by the Rift via a translation layer in SteamVR, and **LibOVR**, by Oculus, supported only by the Rift. Since Valve's API promised to be an open specification that would gather support with time, and worked with the two main headsets one way or the other, we chose to use it in Gaia Sky.

The implementation was quick, and within a week I had a working prototype. The API itself was simple enough, and it was split up into different modules, called interfaces, which handled different aspects of the application lifecycle. Like so, we had ``IVRSystem`` for display, tracking and events, ``IVRCompositor`` for submitting images to the compositor, or ``IVRRenderModels``, which provided controller and headset render models directly from within the runtime. Everything was rather high-level and abstracted. It provided features which are arguably best left to the applications to handle, but it worked. Since the inception of the API until mid-2018, input was handled via events only. Later on, ``IVRInput`` was introduced, which provided an input abstraction layer much like OpenXR's.

A rather scrawny-looking documentation of OpenVR can be found [here](https://github.com/ValveSoftware/openvr/wiki/API-Documentation). The real documentation, though, is in the [header files](https://github.com/ValveSoftware/openvr/blob/master/headers/openvr.h).

In essence, the driver in OpenVR does much of the heavylifting, allowing for an less verbose and more to-the-point API. OpenXR, though, would be different.

## OpenXR

OpenXR, the royalty-free standard for access to VR and AR devices, was announced by the Khronos Group in GDC 2017.[^5] The API itself was and is being developed by a working group containing the main players in the XR space: Microsoft, Google, Oculus/Meta, Valve, Epic, Unity, Collabora and Mozilla, just to name a few. They worked with the aim to create a truly open standard that everyone would adopt and support, and promised to end XR fragmentation. They delivered. 

{{< fig 
    src1="/img/2023/05/xr-fragmentation.jxl" 
    type1="image/jxl" 
    src2="/img/2023/05/xr-fragmentation.avif" 
    type2="image/avif" 
    src="/img/2023/05/xr-fragmentation.png" 
    class="fig-center"
    width="60%" 
    title="Solving XR fragmentation. Source: khronos.org" 
    loading="lazy" >}}

The first version of the OpenXR specification was released at SIGGRAPH 2019.[^6] The result was a well-designed, well-documented and much lower level programming interface that supported a much wider set of use cases and would be more performant than previous efforts. The API contained some key types through which most of the functionality was accessed, like ``XrInstance``, ``XrSession``, ``XrSpace``, ``XrActionSet`` and ``XrAction``.

Also, different vendors were and are encouraged to submit their own extensions to the API in order to cover use cases which are, if not of general interest, still common enough to be present in the specification. The list of current extensions is [vast](https://registry.khronos.org/OpenXR/specs/1.0/html/xrspec.html#extension-appendices-list), and contains functionality that goes from requesting GLTF models from the runtime, to the foveation rendering technique.

Since the release announcement in 2019 I put the "Migration of Gaia Sky VR to OpenXR" item in my TODO list. When the [LWJGL Java bindings to OpenXR](https://github.com/LWJGL/lwjgl3/tree/master/modules/lwjgl/openxr/src/generated/java/org/lwjgl/openxr) came, a bit later in 2021, the stage was ready for the migration to start.

The following sub-sections describe, in more or less detail, the different components of an OpenXR application. When applicable, I will also provide code snippets from the current implementation to illustrate certain actions or concepts. These are in Java, but it should be easy to translate them to C++, C# or even plain C. The descriptions provided below do not aim for completion. Their intention is not to provide a full reference or a complete set of guidelines to write OpenXR applications. The main aim of this part is to provide a bird's eye view of the different components in an OpenXR application, while also describing their purpose, layout and interconnectivity to achieve a cohesive VR application. I know next to nothing about AR, so I won't cover it here. When in doubt, refer to the excellent official [OpenXR documentation pages](https://registry.khronos.org/OpenXR/specs/1.0/html/xrspec.html).


### Runtimes

In OpenXR, just like in most other APIs, there exists the concept of the runtime. The runtime implements the interface and contains the logic to translate API calls to actual hardware commands that a particular device understands. This is usually a program provided by your device vendor. It would be the Meta Quest PC app for Meta headsets, or the SteamVR application for the SteamVR family of devices (Valve Index, HTC Vive(s)). You need to have the runtime running before starting your application, as it will attempt to connect to it. Also, you may have two or more runtimes that implement OpenXR for different devices. In that case, you need to set the default system OpenXR provider in the settings of the runtime of the device you want to use.

### Lifecycle

In my implementation, I created a file called [``XrDriver``](https://codeberg.org/gaiasky/gaiasky/src/commit/f46d32aed5bf7826c4780726789cde7b0347fa16/core/src/gaiasky/vr/openxr/XrDriver.java) which handles most of the talking to the OpenXR API. Parse it quickly, and you will spot methods to create and initialize the OpenXR instance, create the session, create the reference space, and initialize the frame buffers and swapchains. It also manages the creation of the input objects (action spaces and actions). The following sections describe each of these steps in detail.

### Instance Creation

We first need to initialize the connection to an OpenXR runtime using [``XrInstance``](https://registry.khronos.org/OpenXR/specs/1.0/html/xrspec.html#XrInstance). In the instance creation method, I check the API layers available ([layers in OpenXR](https://registry.khronos.org/OpenXR/specs/1.0/html/xrspec.html#api-layers) provide additional functions by intercepting the calls), and I check specifically for the core validation layer. If this is available, we will request it when the instance is created.

``` java
// Get number of layers available.
var pi = stack.mallocInt(1);
boolean hasCoreValidationLayer = false;
check(xrEnumerateApiLayerProperties(pi, null));
int numLayers = pi.get(0);

// Get actual layers.
XrApiLayerProperties.Buffer pLayers 
    = XrHelper.prepareApiLayerProperties(stack, numLayers);
check(xrEnumerateApiLayerProperties(pi, pLayers));
for (int index = 0; index < numLayers; index++) {
    XrApiLayerProperties layer = pLayers.get(index);

    String layerName = layer.layerNameString();
    logger.info("Layer available: " + layerName);
    if (layerName.equals("XR_APILAYER_LUNARG_core_validation")) {
        hasCoreValidationLayer = true;
    }
}

// Prepare a buffer with the required layers, used later at instance creation.
PointerBuffer wantedLayers;
if (hasCoreValidationLayer) {
    wantedLayers = stack.callocPointer(1);
    wantedLayers.put(0, stack.UTF8("XR_APILAYER_LUNARG_core_validation"));
    logger.info(I18n.msg("vr.enable.validation"));
} else {
    wantedLayers = null;
}
```

The ``check()`` function is a utility method that checks that the result of an OpenXR call is ``XR_SUCCEEDED``. If the result is ``XR_FAILED``, it gets the error message from the API, logs it, and throws an exception.

After checking the layers, we ask the runtime to provide a list of implemented extensions that we can use. Particularly, we do our rendering using OpenGL, so the runtime must absolutely support the OpenGL extension:

```java
// Get number of extensions.
check(xrEnumerateInstanceExtensionProperties((ByteBuffer) null, pi, null));
int numExtensions = pi.get(0);

// Create extension properties object.
var properties = XrHelper.prepareExtensionProperties(stack, numExtensions);
check(xrEnumerateInstanceExtensionProperties((ByteBuffer) null, pi, properties));

// Buffer with desired extensions to use later at instance creation.
var wantedExtensions = stack.mallocPointer(1);
boolean missingOpenGL = true;
for (int i = 0; i < numExtensions; i++) {
    XrExtensionProperties prop = properties.get(i);

    var extensionName = prop.extensionNameString();
    logger.info("Extension detected: " + extensionName);
    if (extensionName.equals(XR_KHR_OPENGL_ENABLE_EXTENSION_NAME)) {
        missingOpenGL = false;
        wantedExtensions.put(prop.extensionName());
    }
}
wantedExtensions.flip();

if (missingOpenGL) {
    throw new IllegalStateException("Runtime does not provide required extension: "
        + XR_KHR_OPENGL_ENABLE_EXTENSION_NAME);
}
```

Finally, we are ready to create the OpenXR instance with ``xrCreateInstance()``, which creates the ``XrInstance`` and enables the requested layers and extensions. We also need to pass an application name to this call in order for the runtime to identify the application in its menus or interfaces. ``XrInstance`` is the object that allows our application to talk to the OpenXR runtime, and we'll be using it repeatedly in our calls.

```java
var createInfo = XrInstanceCreateInfo.malloc(stack)
        .type$Default()
        .next(NULL)
        .createFlags(0)
        .applicationInfo(XrApplicationInfo.calloc(stack)
                .applicationName(stack.UTF8("Gaia Sky VR"))
                .apiVersion(XR_CURRENT_API_VERSION))
        .enabledApiLayerNames(wantedLayers)
        .enabledExtensionNames(wantedExtensions);

var pp = stack.mallocPointer(1);
check(xrCreateInstance(createInfo, pp));
var xrInstance = new XrInstance(pp.get(0), createInfo);
```

### System Initialization

Once our instance is ready, we may proceed to create the system. A system in OpenXR represents a group of related devices in the runtime. For instance, if you are using a runtime that supports The Rift and the Vive (with sensors, controllers, etc.), then we can create a system for each of those. Typically, only one system is connected at a time, so we will just attempt to detect and connect to a single HMD system. To that effect, we use the ``XR_FORM_FACTOR_HEAD_MOUNTED_DISPLAY`` property. Each system is represented by a double-precision integer identifier number, which we call ``systemId``.

```java
// Long buffer.
var pl = stack.longs(0);

// Instance properties object, to get some info about the system and runtime.
var properties = XrInstanceProperties.calloc(stack).type$Default();
check(XR10.xrGetInstanceProperties(xrInstance, properties));

// Get name, version and descriptor string.
runtimeName = properties.runtimeNameString();
runtimeVersion = properties.runtimeVersion();
runtimeVersionString = XR10.XR_VERSION_MAJOR(runtimeVersion) 
    + "." + XR10.XR_VERSION_MINOR(runtimeVersion) 
    + "." + XR10.XR_VERSION_PATCH(runtimeVersion);

logger.info("Runtime name: " + runtimeName);
logger.info("Runtime version: " + runtimeVersionString);

// Get actual system identifier.
check(xrGetSystem(xrInstance, XrSystemGetInfo.malloc(stack)
        .type$Default()
        .next(NULL)
        .formFactor(XR_FORM_FACTOR_HEAD_MOUNTED_DISPLAY), pl));

long systemId = pl.get(0);
if (systemId == 0) {
    throw new IllegalStateException("No compatible headset detected");
}
logger.info("Created system with ID: " + systemId);
```

### Session Creation

Now we need to create the OpenXR session, which represents the application's intent to display content to the user. The session object manages the XR lifecycle. The session can be in several states (idle, ready, sycnrhonized, visible, focused, etc.), and transitions between states are described in the following diagram.


{{< fig 
    src="/img/2023/05/xr-session.svg" 
    class="fig-center"
    type="image/svg"
    width="80%" 
    title="The OpenXR session lifecycle. Source: khronos.org" 
    loading="lazy" >}}

The actual session creation is easy enough. We need to create a binding to OpenGL (delegated to ``XrHelper``), prepare the session create information object, and issue the call.

```java
//Bind the OpenGL context to the OpenXR instance and create the session
Struct graphicsBinding = XrHelper.createOpenGLBinding(stack, windowHandle);

var sessionCreateInfo = XrSessionCreateInfo.calloc(stack)
        .set(XR10.XR_TYPE_SESSION_CREATE_INFO,
                graphicsBinding.address(),
                0,
                systemId);

var pp = stack.mallocPointer(1);
check(xrCreateSession(xrInstance, sessionCreateInfo, pp));

var xrSession = new XrSession(pp.get(0), xrInstance);
```

### Reference Space

The runtime maps the location of virtual objects to corresponding real-world locations using spaces. A space is essentially a frame of reference in the real world used by tracking, specified by the application. Three basic reference spaces are defined by OpenXR: view, local, and stage. 

```java
public static final int
    XR_REFERENCE_SPACE_TYPE_VIEW  = 1,
    XR_REFERENCE_SPACE_TYPE_LOCAL = 2,
    XR_REFERENCE_SPACE_TYPE_STAGE = 3;
```

In our case, we use a space of type 'local' as our main application space, which we create like so:

```java
var pp = stack.mallocPointer(1);

check(xrCreateReferenceSpace(xrSession, XrReferenceSpaceCreateInfo.malloc(stack)
        .type$Default()
        .next(NULL)
        .referenceSpaceType(XR_REFERENCE_SPACE_TYPE_LOCAL)
        .poseInReferenceSpace(XrPosef.malloc(stack)
                .orientation(XrQuaternionf.malloc(stack)
                        .x(0)
                        .y(0)
                        .z(0)
                        .w(1))
                .position$(XrVector3f.calloc(stack))), pp));

var xrAppSpace = new XrSpace(pp.get(0), xrSession);
```

As you can see, we need a pose in the natural reference frame defined by the space type. We use the simple quaternion \\([0, 0, 0, 1]\\) as our pose.

### Swapchains

In order to present images to the user, the runtime provides images organized in swapchains that the application can render into. Swapchains are simple sequences of image buffers with a certain format that we will later use as render targets in the render stage of our XR renderer.

The creation of swapchains is a bit more involved than what we have seen so far, but with a little dedication and with the help of the official specification, we can get it working:

```java
var pi = stack.mallocInt(1);

check(xrEnumerateViewConfigurationViews(xrInstance, 
                                        systemId, 
                                        viewConfigType, 
                                        pi, 
                                        null));
viewConfigs = XrHelper.fill(XrViewConfigurationView.calloc(pi.get(0)), 
        XrViewConfigurationView.TYPE, XR_TYPE_VIEW_CONFIGURATION_VIEW);

check(xrEnumerateViewConfigurationViews(xrInstance, 
                                    systemId, 
                                    viewConfigType, 
                                    pi, 
                                    viewConfigs));
int viewCountNumber = pi.get(0);

views = XrHelper.fill(XrView.calloc(viewCountNumber), XrView.TYPE, XR_TYPE_VIEW);

if (viewCountNumber > 0) {
    check(xrEnumerateSwapchainFormats(xrSession, pi, null));
    var swapchainFormats = stack.mallocLong(pi.get(0));
    check(xrEnumerateSwapchainFormats(xrSession, pi, swapchainFormats));

    long[] desiredSwapchainFormats = {
            GL_SRGB8_ALPHA8,
            GL_RGB10_A2,
            GL_RGBA16F,
            // The two below should only be used as a fallback,
            // as they are linear color formats without enough bits for color
            // depth, thus leading to banding.
            GL_RGBA8,
            GL31.GL_RGBA8_SNORM };

    out:
    for (long glFormatIter : desiredSwapchainFormats) {
        for (int i = 0; i < swapchainFormats.limit(); i++) {
            if (glFormatIter == swapchainFormats.get(i)) {
                glColorFormat = glFormatIter;
                break out;
            }
        }
    }

    if (glColorFormat == 0) {
        throw new IllegalStateException("No compatable swapchain format availible");
    }

    swapChains = new SwapChain[viewCountNumber];
    for (int i = 0; i < viewCountNumber; i++) {
        XrViewConfigurationView viewConfig = viewConfigs.get(i);

        var swapchainWrapper = new SwapChain();

        var swapchainCreateInfo = XrSwapchainCreateInfo.malloc(stack)
                .type$Default()
                .next(NULL)
                .createFlags(0)
                .usageFlags(XR_SWAPCHAIN_USAGE_SAMPLED_BIT 
                    | XR_SWAPCHAIN_USAGE_COLOR_ATTACHMENT_BIT)
                .format(glColorFormat)
                    .sampleCount(viewConfig.recommendedSwapchainSampleCount())
                .width(viewConfig.recommendedImageRectWidth())
                .height(viewConfig.recommendedImageRectHeight())
                .faceCount(1)
                .arraySize(1)
                .mipCount(1);

        var pp = stack.mallocPointer(1);
        check(xrCreateSwapchain(xrSession, swapchainCreateInfo, pp));

        swapchainWrapper.handle = new XrSwapchain(pp.get(0), xrSession);
        swapchainWrapper.width = swapchainCreateInfo.width();
        swapchainWrapper.height = swapchainCreateInfo.height();

        check(xrEnumerateSwapchainImages(swapchainWrapper.handle, pi, null));
        int imageCount = pi.get(0);

        XrSwapchainImageOpenGLKHR.Buffer swapchainImageBuffer = 
            XrHelper.fill(XrSwapchainImageOpenGLKHR.create(imageCount),
                        XrSwapchainImageOpenGLKHR.TYPE, 
                        XR_TYPE_SWAPCHAIN_IMAGE_OPENGL_KHR);

        check(xrEnumerateSwapchainImages(swapchainWrapper.handle, 
                        pi, 
                        XrSwapchainImageBaseHeader.create(swapchainImageBuffer.address(), 
                                                        swapchainImageBuffer.capacity())));
        swapchainWrapper.images = swapchainImageBuffer;
        swapChains[i] = swapchainWrapper;
    }
}
```

### Input

Finally, we have the base OpenXR instance initialized and we can start thinking about how to handle input from VR controllers. The input and haptics system in OpenXR contains several abstractions that make it easier to remap actual physical buttons and joysticks to application actions at the runtime level. To that effect, OpenXR defines action sets, actions and interaction profiles.

- **Action sets** are groups of actions attached to a particular session. Each action set is intended to be active or not depending on the context. For example, we may have an action set for the user interface and an action set for the regular interaction with the 3D scene. In Gaia Sky we have a very simple input model, so we'll only use one action set.
- **Actions** refer to individual concrete actions within the application, that can be bound to physical inputs in input devices, like buttons or joysticks.
- **Interaction profiles** define suggested action bindings for known devices. For instance, you can provide the bindings for the Oculus Touch controllers and for the Valve Index via interaction profiles. These can be remapped later on by the user at runtime level. 


Action sets are created with a name, a localized name, and a priority:

```java
// Create action set with given name and localized name.
XrActionSetCreateInfo setCreateInfo = XrActionSetCreateInfo.malloc(stack)
        .type$Default()
        .actionSetName(stack.UTF8(name))
        .localizedActionSetName(stack.UTF8(localizedName))
        .priority(priority);

PointerBuffer pp = stack.mallocPointer(1);
driver.check(xrCreateActionSet(driver.xrInstance, setCreateInfo, pp));
var actionSet = new XrActionSet(pp.get(0), driver.xrInstance);
```

There are five action types, described in the API by the following integer values: 

```java
    public static final int
        XR_ACTION_TYPE_BOOLEAN_INPUT    = 1,
        XR_ACTION_TYPE_FLOAT_INPUT      = 2,
        XR_ACTION_TYPE_VECTOR2F_INPUT   = 3,
        XR_ACTION_TYPE_POSE_INPUT       = 4,
        XR_ACTION_TYPE_VIBRATION_OUTPUT = 100;
```

These map to the following action types:

- **Boolean actions**, used for boolean inputs, like buttons, that have an on/off state.
- **Float actions**, used for inputs that have a range of one-dimensional floating-point values, like analog trigger buttons.
- **Float-2 actions**, used for inputs that have a range of two-dimensional floating-point values, like joysticks.
- **Pose actions**, used to get orientation information from a tracked VR device like a controller.
- **Haptic output actions**, used to send haptic pulses (rubmle) to a device.

Actions are initialized by calling ``xrCreateAction`` with an ``XrActionCreateInfo`` object, which contains the name and localized name of the action, plus the type.

```java
// Create action with given name, localized name, and type.
// The action will be created as a part of the given action set.
XrActionCreateInfo createInfo = XrActionCreateInfo.malloc(stack)
        .type$Default()
        .next(NULL)
        .actionName(stack.UTF8(name))
        .localizedActionName(stack.UTF8(localizedName))
        .countSubactionPaths(0)
        .actionType(type);

PointerBuffer pp = stack.mallocPointer(1);
driver.check(xrCreateAction(actionSet, createInfo, pp));
var action =  new XrAction(pp.get(0), actionSet);
```

Every frame, we need synchronize the action set and all the actions.

```java
// Sync action set.
XrActiveActionSet.Buffer sets = XrActiveActionSet.calloc(1, stack);
sets.actionSet(actions.getHandle());

XrActionsSyncInfo syncInfo = XrActionsSyncInfo.calloc(stack)
        .type(XR_TYPE_ACTIONS_SYNC_INFO).activeActionSets(sets);

check(xrSyncActions(xrSession, syncInfo));
if (actions != null) {
    // Sync all actions in the action set.
    // This depends on the action type!
    actions.sync(this);

    // All actions have the updated state here.
    // Send input to listeners so that things happen in the application.
    // This is Gaia Sky specific, hence not important.
    var gsActions = (GaiaSkyActionSet) actions;
    for (var listener : listeners) {
        gsActions.processListener(listener);
    }
}

```

Syncing actions means updating their state. The code to sync an action depends on the action type. For example, boolean actions (for VR controller buttons) are synced using ``xrGetActionStateBoolean()``, with the session, an ``XrActionStateGetInfo`` instance, and a ``XrActionStateBoolean`` object, which will be updated with the new state. After this is called, the ``XrActionStateBoolean#currentState()`` method returns true if the button currently bound to that action is pressed, and false otherwise.

More interesting are the **pose actions**, which are used to update the position and orientation of VR controllers. Pose actions need a specific action space for tracking the position of the device. Synchronizing a pose action is only a little bit more involved:

```java
driver.check(XR10.xrGetActionStatePose(driver.xrSession, getInfo, state),
            "xrGetActionStatePose");
controllerDevice.active = state.isActive();
if (controllerDevice.active && driver.currentFrameTime > 0) {
    location.set(XR_TYPE_SPACE_LOCATION, NULL, 0, pose);
    driver.checkNoException(
        xrLocateSpace(space, 
                        driver.xrAppSpace, 
                        driver.currentFrameTime, 
                        location));
    if ((location.locationFlags() 
            & XR_SPACE_LOCATION_POSITION_VALID_BIT) != 0
            && (location.locationFlags() 
                & XR_SPACE_LOCATION_ORIENTATION_VALID_BIT) != 0) {
        // Ok!
        if (poseType.isGrip()) {
            controllerDevice.setGripPose(location.pose());
        } else {
            controllerDevice.setAim(location.pose());
        }
    }
}

```

The ``controllerDevice`` is an object representing a VR controller. Since OpenXR offers two pose types per VR controller device (grip, at the hand grip, and aim, at the pointy end), we have cases for each.

{{< fig 
    src="/img/2023/05/xr-grip-aim.png" 
    class="fig-center"
    width="70%" 
    title="Grip and aim poses in OpenXR. Source: khronos.org" 
    loading="lazy" >}}

The pose object that we pass into the controller device has methods to get the position (3-vector) and orientation (quaternion), so building its transformation matrix is quite straightforward.

Finally, when initializing the actions and action sets we are encouraged to submit interaction profiles, which contain suggested bindings. I store them in a set of maps (one for each supported device) at the action set level:

```java
// Oculus touch.
map.computeIfAbsent("/interaction_profiles/oculus/touch_controller", 
    aLong -> new ArrayList<>()).addAll(
    List.of(
            new Pair<>(deviceLeft.aimPose, "/user/hand/left/input/aim/pose"),
            new Pair<>(deviceRight.aimPose, "/user/hand/right/input/aim/pose"),

            new Pair<>(deviceLeft.gripPose, "/user/hand/left/input/grip/pose"),
            new Pair<>(deviceRight.gripPose, "/user/hand/right/input/grip/pose"),

            new Pair<>(deviceLeft.haptics, "/user/hand/left/output/haptic"),
            new Pair<>(deviceRight.haptics, "/user/hand/right/output/haptic"),

            new Pair<>(deviceLeft.showUi, "/user/hand/left/input/y/click"),
            new Pair<>(deviceRight.showUi, "/user/hand/right/input/b/click"),

            new Pair<>(deviceLeft.accept, "/user/hand/left/input/y/click"),
            new Pair<>(deviceRight.accept, "/user/hand/right/input/b/click"),

            new Pair<>(deviceLeft.cameraMode, "/user/hand/left/input/x/click"),
            new Pair<>(deviceRight.cameraMode, "/user/hand/right/input/a/click"),

            new Pair<>(deviceLeft.select, "/user/hand/left/input/trigger/value"),
            new Pair<>(deviceRight.select, "/user/hand/right/input/trigger/value"),

            new Pair<>(deviceLeft.move, "/user/hand/left/input/thumbstick"),
            new Pair<>(deviceRight.move, "/user/hand/right/input/thumbstick")
    ));

// Valve Index.
map.computeIfAbsent("/interaction_profiles/valve/index_controller", 
    aLong -> new ArrayList<>()).addAll(
    List.of(
            new Pair<>(deviceLeft.aimPose, "/user/hand/left/input/aim/pose"),
            new Pair<>(deviceRight.aimPose, "/user/hand/right/input/aim/pose"),

            new Pair<>(deviceLeft.gripPose, "/user/hand/left/input/grip/pose"),
            new Pair<>(deviceRight.gripPose, "/user/hand/right/input/grip/pose"),

            new Pair<>(deviceLeft.haptics, "/user/hand/left/output/haptic"),
            new Pair<>(deviceRight.haptics, "/user/hand/right/output/haptic"),

            new Pair<>(deviceLeft.showUi, "/user/hand/left/input/b/click"),
            new Pair<>(deviceRight.showUi, "/user/hand/right/input/b/click"),

            new Pair<>(deviceLeft.accept, "/user/hand/left/input/b/click"),
            new Pair<>(deviceRight.accept, "/user/hand/right/input/b/click"),

            new Pair<>(deviceLeft.cameraMode, "/user/hand/left/input/a/click"),
            new Pair<>(deviceRight.cameraMode, "/user/hand/right/input/a/click"),

            new Pair<>(deviceLeft.select, "/user/hand/left/input/trigger/value"),
            new Pair<>(deviceRight.select, "/user/hand/right/input/trigger/value"),

            new Pair<>(deviceLeft.move, "/user/hand/left/input/thumbstick"),
            new Pair<>(deviceRight.move, "/user/hand/right/input/thumbstick")
    ));

// HTC Vive.
map.computeIfAbsent("/interaction_profiles/htc/vive_controller", 
    aLong -> new ArrayList<>()).addAll(
    List.of(
            new Pair<>(deviceLeft.aimPose, "/user/hand/left/input/aim/pose"),
            new Pair<>(deviceRight.aimPose, "/user/hand/right/input/aim/pose"),

            new Pair<>(deviceLeft.gripPose, "/user/hand/left/input/grip/pose"),
            new Pair<>(deviceRight.gripPose, "/user/hand/right/input/grip/pose"),

            new Pair<>(deviceLeft.haptics, "/user/hand/left/output/haptic"),
            new Pair<>(deviceRight.haptics, "/user/hand/right/output/haptic"),

            new Pair<>(deviceLeft.showUi, "/user/hand/left/input/menu/click"),
            new Pair<>(deviceRight.showUi, "/user/hand/right/input/menu/click"),

            new Pair<>(deviceLeft.accept, "/user/hand/left/input/menu/click"),
            new Pair<>(deviceRight.accept, "/user/hand/right/input/menu/click"),

            new Pair<>(deviceLeft.cameraMode, "/user/hand/left/input/trackpad/click"),
            new Pair<>(deviceRight.cameraMode, "/user/hand/right/input/trackpad/click"),

            new Pair<>(deviceLeft.select, "/user/hand/left/input/trigger/value"),
            new Pair<>(deviceRight.select, "/user/hand/right/input/trigger/value"),

            new Pair<>(deviceLeft.move, "/user/hand/left/input/trackpad"),
            new Pair<>(deviceRight.move, "/user/hand/right/input/trackpad")
    ));
```

As you can see, I have three maps, for the Oculus, the Valve Index the HTC Vive controllers respectively. The first component in each pair is the action, and the second is an interaction profile path identifying a specific input or output mechanism. More info on this [here](https://registry.khronos.org/OpenXR/specs/1.0/html/xrspec.html#semantic-path-input). Finally, these pairs can be submitted to OpenXR in the following way:

```java
var devices = bindingsMap.keySet();
for (var device : devices) {
    var bindings = bindingsMap.get(device);
    XrActionSuggestedBinding.Buffer bindingsBuffer =
        XrActionSuggestedBinding.calloc(bindings.size(), stack);
    int l = 0;
    for (var binding : bindings) {
        bindingsBuffer.get(l++).set(
                binding.getA().getHandle(),
                getPath(binding.getB()));
    }

    XrInteractionProfileSuggestedBinding suggestedBinding = 
        XrInteractionProfileSuggestedBinding.malloc(stack)
            .type$Default()
            .next(NULL)
            .interactionProfile(getPath(device))
            .suggestedBindings(bindingsBuffer);
    check(xrSuggestInteractionProfileBindings(xrInstance, suggestedBinding));
}

// Attach action set to session.
XrSessionActionSetsAttachInfo attachInfo =
    XrSessionActionSetsAttachInfo.calloc(stack).set(
        XR_TYPE_SESSION_ACTION_SETS_ATTACH_INFO,
        NULL,
        stackPointers(actions.getHandle()));
check(xrAttachSessionActionSets(xrSession, attachInfo));

```

Where ``devices`` is a list containing a map for each device, and ``binding`` is a single pair of action-binding for a specific device.


### Rendering Cycle

The main loop in the application reads OpenXR events in a cycle with ``xrPollEvent(instance, buff)`` until no events are left to process. Special events are processed on the spot (instance loss, state changed, reference space change pending, etc.). Rendering also happens every frame in the main loop, of course. In my implementation, rendering is a back-and-forth business between the ``XrDriver`` and the renderer. The driver prepares the frame, gets the predicted time, issues the commands to render each layer, and ends the frame.

```java
// Get frame state object.
XrFrameState frameState = getFrameState(stack);

// Issue begin frame call.
check(xrBeginFrame(xrSession, XrFrameBeginInfo.calloc(stack).type$Default()));

XrCompositionLayerProjection layerProjection = 
    XrCompositionLayerProjection.calloc(stack).type$Default();

var layers = stack.callocPointer(1);
boolean didRender = false;

// Fetch predicted frame time.
currentFrameTime = frameState.predictedDisplayTime();

// Render each layer.
if (frameState.shouldRender()) {
    if (renderLayerOpenXR(stack, currentFrameTime, layerProjection)) {
        layers.put(0, layerProjection.address());
        didRender = true;
    }
}

// End frame.
check(xrEndFrame(xrSession, XrFrameEndInfo.malloc(stack)
        .type$Default()
        .next(NULL)
        .displayTime(currentFrameTime)
        .environmentBlendMode(XR_ENVIRONMENT_BLEND_MODE_OPAQUE)
        .layers(didRender ? layers : null)
        .layerCount(didRender ? layers.remaining() : 0)));


```

The ``renderLayerOpenXR()`` method renders a single layer. For each layer we need to render a set of views, usually one view per eye. To do so, we first get the view swapchain for the current view and acquire the image index. This is used to get the buffer that we need to render to. 

```java
XrViewState viewState = XrViewState.calloc(stack).type$Default();

IntBuffer pi = stack.mallocInt(1);
check(xrLocateViews(xrSession, 
                XrViewLocateInfo.malloc(stack)
                    .type$Default()
                    .next(NULL)
                    .viewConfigurationType(viewConfigType)
                    .displayTime(predictedDisplayTime)
                    .space(xrAppSpace), 
                viewState, 
                pi, 
                views));

if ((viewState.viewStateFlags() 
    & XR_VIEW_STATE_POSITION_VALID_BIT) == 0 
    || (viewState.viewStateFlags() 
    & XR_VIEW_STATE_ORIENTATION_VALID_BIT) == 0) {
    return false;  // There is no valid tracking poses for the views.
}

int viewCountOutput = pi.get(0);
assert (viewCountOutput == views.capacity());
assert (viewCountOutput == viewConfigs.capacity());
assert (viewCountOutput == swapChains.length);

XrCompositionLayerProjectionView.Buffer projectionLayerViews 
    = XrHelper.fill(XrCompositionLayerProjectionView
                                    .calloc(viewCountOutput, stack),
                    XrCompositionLayerProjectionView.TYPE, 
                    XR_TYPE_COMPOSITION_LAYER_PROJECTION_VIEW);

// Render view to the appropriate part of the swapchain image.
for (int viewIndex = 0; viewIndex < viewCountOutput; viewIndex++) {
    // Each view has a separate swapchain which is acquired, rendered to, and released.
    SwapChain viewSwapchain = swapChains[viewIndex];

    check(xrAcquireSwapchainImage(viewSwapchain.handle, 
                        XrSwapchainImageAcquireInfo.calloc(stack)
                                                    .type$Default(), 
                        pi));
    int swapchainImageIndex = pi.get(0);

    check(xrWaitSwapchainImage(viewSwapchain.handle, 
                                XrSwapchainImageWaitInfo.malloc(stack)
                                        .type$Default()
                                        .next(NULL)
                                        .timeout(XR_INFINITE_DURATION)));

    XrCompositionLayerProjectionView projectionLayerView = projectionLayerViews
                .get(viewIndex)
                .pose(views.get(viewIndex).pose())
                .fov(views.get(viewIndex).fov())
                .subImage(si -> si.swapchain(viewSwapchain.handle)
                                    .imageRect(rect -> rect.offset(offset ->    
                                                                        offset.x(0).y(0))
                                    .extent(extent -> extent.width(viewSwapchain.width)
                                                            .height(viewSwapchain.height))));

    if (currentRenderer.get() != null) {
        currentRenderer.get().renderOpenXRView(projectionLayerView, 
                                            viewSwapchain.images.get(swapchainImageIndex),
                                            viewFrameBuffers == null ? 
                                                            null : 
                                                            viewFrameBuffers[viewIndex],
                                            viewIndex);
    }

    check(xrReleaseSwapchainImage(viewSwapchain.handle, 
                                    XrSwapchainImageReleaseInfo.calloc(stack).
                                            type$Default()));
}

layer.space(xrAppSpace);
layer.views(projectionLayerViews);
```

The actual rendering in Gaia Sky VR is handled by the ``currentRenderer`` object, which is of type ``XrRenderer``. This is an interface that defines a single method to render one view:

```java
/**
 * Executed for each eye every cycle.
 *
 * @param layerView      The layer view.
 * @param swapchainImage The swapchain image.
 * @param frameBuffer    The frame buffer to draw to.
 * @param viewIndex      The view index.
 */
void renderOpenXRView(XrCompositionLayerProjectionView layerView,
                          XrSwapchainImageOpenGLKHR swapchainImage,
                          FrameBuffer frameBuffer,
                          int viewIndex);

```

The implementation in a simple renderer looks like this:

```java
public void renderOpenXRView(XrCompositionLayerProjectionView layerView, 
                            XrSwapchainImageOpenGLKHR swapchainImage, 
                            FrameBuffer frameBuffer, 
                            int viewIndex) {
    // Update camera with view position and orientation.
    viewManager.updateCamera(layerView, camera);

    frameBuffer.begin();

    // Attach swapchain image to frame buffer.
    glFramebufferTexture2D(GL_FRAMEBUFFER, 
                        GL_COLOR_ATTACHMENT0, 
                        GL_TEXTURE_2D, 
                        swapchainImage.image(), 
                        0);

    // Actual rendering.
    // This is stub code that uses a batch to render a single model.
    Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT | GL20.GL_DEPTH_BUFFER_BIT);
    batch.begin(camera);
    batch.render(instance, uiEnvironment);
    batch.end();

    frameBuffer.end();

    // Render to screen if necessary.
    if (viewIndex == 0 && renderToScreen) {
        // Set to texture view for rendering to screen.
        textureView.setTexture(swapchainImage.image(), 
                                driver.getWidth(), 
                                driver.getHeight());
        Gdx.gl.glEnable(GL40.GL_FRAMEBUFFER_SRGB);
        RenderUtils.renderKeepAspect(textureView, sbScreen, Gdx.graphics, lastSize);
        Gdx.gl.glDisable(GL40.GL_FRAMEBUFFER_SRGB);
    }
}
```

I have left out unimportant things in this snippet. First, we use our ``viewManager`` to update the camera. In this method, we use the ``layerView`` to get the pose, and with that, the position and orientation of the headset. Once we have the position as a 3-vector and the orientation quaternion, we just set it to our internal camera.

```java
public void updateCamera(XrCompositionLayerProjectionView layerView,
                             PerspectiveCamera camera,
                             NaturalCamera naturalCamera,
                             RenderingContext rc) {
    XrPosef pose = layerView.pose();
    XrVector3f position = pose.position$();
    XrQuaternionf orientation = pose.orientation();

    // Use position and orientation to update camera.
    ...
}
```

After the camera is prepared for the current view, we attach swapchain image to the current frame buffer used for rendering with ``glFramebufferTexture2D()``. Then, we just need to render the scene normally. Finally, I also want to render to the screen, so I take what's in the frame buffer of the first view and render it to the display. Once control is returned to the driver, the swapchain images have the rendered contents and can be released, and the frame ended. The images are ready to be presented to the user by the headset.

## Conclusions

In this post, we have explored the overall structure of an application using OpenXR, how to initialize the instance and system, how to handle input and how to do the rendering. OpenXR is widely supported by the industry and community, performs better, is well-documented, and is far more future-proof than any of the previously existing, vendor-locked, competing APIs. The first Gaia Sky version after the migration to OpenXR will be 3.5.0, which will be available very soon. In the mean time, you can try it out by downloading one of the release candidates [here](https://gaia.ari.uni-heidelberg.de/gaiasky/files/releases/release_candidates/3.5.0/).

[^1]: actually, it is possible to use a translation layer like [OpenComposite](https://gitlab.com/znixian/OpenOVR), which translates calls from OpenVR to a modern API like OpenXR.
[^2]: OpenXR documentation pages: https://registry.khronos.org/OpenXR/specs/1.0/html/xrspec.html
[^3]: LWJGL3, the LightWeight Java Gaming Library: https://www.lwjgl.org
[^4]: MCXR GitHub: https://github.com/mcxr-org/MCXR
[^5]: OpenXR announcement at GDC 2017: https://www.khronos.org/news/press/khronos-reveals-api-updates-new-workgroups-at-gdc
[^6]: OpenXR 1.0 release at SIGGRAPH 2019: https://www.khronos.org/news/press/khronos-releases-openxr-1.0-specification-establishing-a-foundation-for-the-ar-and-vr-ecosystem
