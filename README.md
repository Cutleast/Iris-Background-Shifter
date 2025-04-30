# Iris Background Shifter

While searching on the Internet I did not find any app or tool that changes the Desktop wallpaper according to the currently played game,
so I came up with this project: A tool that runs in the background and changes the Desktop wallpaper depending on the last started game.

While the tool itself is working, it is not very user friendly at the moment: no GUI, index.json has to be edited manually, limited configuration.

## What it does

Whenever an executable that's entered in the index.json is started, Iris will take a random picture from the folder specified in the index.json for that
specific game and set it as wallpaper.

## How to

1. Create an index.json file in the folder where the iris.exe is or just start the iris.exe once and it will create it for you.
    - The location of the index.json does not have to be besides the iris.exe but must be specified when starting the iris.exe if it differs from `./data/index.json`: `iris.exe -i "C:\\path\\to\\index.json"`
2. Put wallpapers/pictures fitting the games you play into separate folders
3. Enter the name of the game's executable and the path to the folder with the pictures for it in the index.json. For example:

    ```json
    {
        "SkyrimSE.exe": "C:\\Users\\User\\Pictures\\Wallpapers\\Skyrim Special Edition",
    }
    ```

4. Optional: In order to add the tool to the autostart create a link to the iris.exe and put it in `shell:startup`.

## Compatibility

Setting the wallpaper only works on Windows, at the moment. Support for other operating systems is not planned.

## Contributing

Feel free to create issues, pull requests or fork this repository entirely!
