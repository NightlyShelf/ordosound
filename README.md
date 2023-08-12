# OrdoSound <img src="icon.ico" alt="icon" width="32"/>
Having a chaos in your music folder? Corrupted music metadata, bad filenames and unhandy folders? This tool will help you to deal with it! 

## Usage

---
**MP3 files only!**

Run in console as ``main.exe {path} y/n``, where {path} is a path to the target folder or file **in quotes**. If your target is a directory, second argument allows working with subdirectories. 

## Example

---
```commandline
main.exe "C:\Music\" y
```
Will fix the music files in ``C:\Music\`` and in all subdirectories like ``C:\Music\Metal\``.

---

```commandline
main.exe "C:\Music\track1.mp3"
```
For a single file.

## Tests

---

Tested only on Windows with NTFS and FAT32 filesystems, but may work on other platforms.