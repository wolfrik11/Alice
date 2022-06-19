@echo off

call %~dp0venv\Scripts\activate

cd %~dp0bot\

set TOKEN=OTU0NzQwOTE5MDc1MjA5MjQ2.GDi8yJ.TggpUhRNqtWdTfnz-dKFwCgHjtXoQzsfzQ0UKk

python start.py

pause