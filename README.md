# SCEWIN / AMISCE

SCEWIN is a tool to modify BIOS NVRAM variables including options that are not visible through UEFI. As far as I know, it is exclusively shipped with MSI Center. This repository was created to provide the SCEWIN binaries without installing the MSI bloatware so that you don't have to.

## Usage

1. Run the ``Export.bat`` script to export NVRAM setting values to ``nvram.txt``

2. Depending on the type of variable, move the ``*`` to the desired option or change the value

3. Run the ``Import.bat`` script to write the configuration in ``nvram.txt`` to NVRAM

## Solutions for various error messages

To determine the error message, a ``log-file.txt`` is generated while running either ``Export.bat``or ``Import.bat`` containg the output messages.

The error codes can be divided into 3 categories:

1. [Both](#both)
2. [Export](#export)
3. [Import](#import)

## Both

### LoadDeviceDriver returned false | Error:1 Unable to load Driver | 10 - Error: Unable to load the driver

This error occurs only in 2 cases:

1. When the drivers (originally named ``amifldrv64.sys`` and ``amigendrv64.sys``) is not in the same folder where **SCEWIN_64.exe** is located
2. The command wasn't run with admin rights - privileges

To fix this error:

1. Be sure that the folder contains both *amifldrv64.sys* and *amigendrv64.sys*
2. Be sure to run **cmd** with admin rights - privileges

### ERROR:57 - Parsing CMD Line Arguments | ERROR:57 - Opening NVRAM Script File

This error only occurs if the command used is incorrect / doesn't exist

To fix this error:

- Verify that the command is correct
- When *importing*, make sure that the **"NVRAM script file"** exists and has the same name as specified in the command

## Export

### WARNING: HII data does not have setup questions information

- If you have an *ASUS* motherboard go [here](#asus)

This error usually occurs when HII resources aren't getting published, therefore there is no data for the program to work with

I have not yet developed a solution for non-ASUS motherboards -- working on it

### ERROR:4 - Retrieving HII Database | ERROR:4 -  BIOS not compatible | ERROR:82 - Retrieving HII Database | ERROR:82 -  BIOS not compatible

This error occurs in multiple cases:

1. As the error message states, the BIOS may not be compatible -- this can only happen if the BIOS is not from **AMI** --> therefore it won't work with any of AMI's tools

- In order to check for BIOS manufacturer:
  - Paste this command in **cmd**:

```bat
systeminfo | findstr /I /C:BIOS
```

- If the vendor listed is "American Megatrends Inc." or "AMI" then you have an AMI BIOS
- If the vendor listed is a different company, then you do not have an AMI BIOS

2. This error usually occurs when the *SmiVariable* is absent or is an older version

- Verify with [UEFITool](https://github.com/LongSoft/UEFITool) whether the module is absent or not
  
  - If it's absent, you can try [inserting](https://winraid.level1techs.com/t/guide-how-to-extract-insert-replace-efi-bios-modules-by-using-the-uefitool/32122) the module (obtain it from another BIOS -- preferably from the same manufacturer)
  - If it's present, you can try [updating](https://winraid.level1techs.com/t/guide-how-to-extract-insert-replace-efi-bios-modules-by-using-the-uefitool/32122) the module (obtain it from another BIOS -- preferably from the same manufacturer)

3. Newer boards only work with the newer versions and display this error while using older versions of SCEWIN (e.g. *ver 5.03.1115*)

### Platform identification failed

Platform identification depends on the *ACPI module label* (for Aptio V)

AMISCE requires Aptio core version **5.008+** for UEFI 2.3

To fix this error:

- You may override this error with ``/d`` option  

```bat
SCEWIN_64.exe /O /S nvram.txt /d
```

## Import

### Warning: Error in writing variable \<variable\> to NVRAM

- If you have an *ASUS* motherboard (Z790+ / B760+ / H770+) go [here](#asus)
- If you have an *ASRock* motherboard (Z590+ / B560+ / H510+) go [here](#asrock)

This error occurs in multiple cases:

1. The variable to be updated is write-protected

2. ``PCI Device`` has been disabled in Device Manager

    - Open Device Manager by typing ``devmgmt.msc`` in ``Win+R``
    - Navigate to ``Other devices``
    - Ensure that **all** ``PCI Device``s are enabled

I have not yet developed a solution regarding variable write-protection for non-ASUS/ASRock motherboards -- working on it

### System configuration not modified

This error occurs in multiple cases:

1. You imported the *NVRAM script file* back unchanged, therefore SCEWIN didn't have to modify anything

2. SCEWIN was unable to apply the changes you made

   - This is related to the [previous error](#warning-error-in-writing-variable-variable-to-nvram)

### Warning in line \<xxxx\> | Missing Current Setting "*"

- Where xxxx is the line number of the input script where the error was detected

### Warning: Unmatched question... prompt: 'Setup Question', Token:' '

- These two errors are related

Search for the **token** in *nvram.txt* and you will see that no value is specified (no \"\*" next to either option). The line specified in the error message (xxxx) is the same as the line of the last option in the *Setup question*, whose **token** we just searched for.

- See [media/error-message-example.png](/media/error-message-example.png)

To fix this error:

1. Put a "*" next to the value that "BIOS Default" suggests

2. You can use the ``/q`` option to suppress *all* warning messages

   ```bat
   SCEWIN_64.exe /I /S nvram.txt /q
   ```

    - This warning message will not appear when importing, along with other (perhaps) useful ones

### WARNING: Length of string for control '\<Setup Question\>' not updated as the value/defaults specified in the script file doesn't reach the minimum range (\<value\>)

- The string given in the script is shorter than the minimum length specified in *NVRAM external defaults* (most likely)
- The usual cause for this is that the string has an initial empty value

**Do not change the value of the string!**

To fix this error:

1. You can use the ``/q`` option to suppress *all* warning messages

   ```bat
   SCEWIN_64.exe /I /S nvram.txt /q
   ```

    - This warning message will not appear when importing, along with other (perhaps) useful ones

2. Don't bother with it -- leave it as is

### ASUS

- If you have an ASUS motherboard (Z590+ / B560+ / H510+) follow these steps:

1. Go to **Setup > Tool** section of your BIOS
2. Enable **_Publish HII Resources_**

This way HII data will be published to the driver --> SCEWIN should work flawlessly

- This section is only required if you have a Z790+ / B760+ board

  - These motherboards require an additional workaround as they password protect the various runtime variables

  - After following the above mentioned steps, you need to **disable** *Password protection of Runtime Variables*

In order to do so, follow these steps:

1. Go to **Setup > Advanced > UEFI Variables Protection** section of your BIOS
2. Disable **_Password protection of Runtime Variables_**

### ASRock

- If you have an ASRock motherboard (Z590+ / B560+ / H510+) follow these steps

  - These motherboards require an additional workaround as they password protect the various runtime variables

In order to do so, follow these steps:

1. Go to **Setup > Advanced > UEFI Variables Protection** section of your BIOS
2. Disable **_Password protection of Runtime Variables_**

- To access this setting, you need to mod your BIOS
  
  - See [UEFI Editor](https://boringboredom.github.io/UEFI-Editor/)

- ASRock's BIOS has 2 Advanced forms --> you need to do a "[Menu swap](https://github.com/BoringBoredom/UEFI-Editor#menu)" in order to gain access to the setting

## Issues

Additional error messages or possible non-working solutions should be reported in the [issue tracker](https://github.com/amitxv/SCEWIN/issues)

Complete the appropriate *issue template*. Consider whether your problem is covered by an existing issue: if so, follow the discussion there. Avoid commenting on existing recurring issues, as such comments do not contribute to the discussion of the issue and may be treated as spam.
