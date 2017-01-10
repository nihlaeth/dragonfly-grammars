#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Half of the speech password module

This part encrypt passwords with a passphrase,
so you can unlock them using speech recognition.
"""
import argparse
from getpass import getpass
from pathlib2 import Path
from simplecrypt import encrypt

def encrypt_password():
    """
    Encrypt password with passphrase provided on command line.

    Store crypt text in files in user directory.

    Raises
    ------
    None

    Returns
    -------
    None

    Examples
    --------
    ..doctest::

        >>> TODO
    """
    #####################
    #  argument parser  #
    #####################
    parser = argparse.ArgumentParser(
        prog="speechpass",
        description="encrypt passwords for use with speech recognition")
    parser.add_argument(
        'language',
        default='enx',
        help="speech language for passphrase")
    parser.add_argument(
        'name',
        help=(
            "name of password, also speech command "
            "(underscores are converted to spaces)"))
    arguments = parser.parse_args()
    #####################
    #  paths and files  #
    #####################
    data_path = Path().home().joinpath(
        'speechpass')
    data_path.mkdir(exist_ok=True)
    language_path = data_path.joinpath(arguments.language)
    language_path.mkdir(exist_ok=True)
    file_path = language_path.joinpath(arguments.name)
    if file_path.exists():
        print "abort: file {} already exists".format(
            file_path)
        return
    #############
    #  secrets  #
    #############
    print "provide password you want to encrypt"
    secret = getpass()
    print "repeat to be sure"
    confirm = getpass()
    if secret != confirm:
        print "passwords do not match"
        return
    print "provide passphrase you want to speak to access your password"
    passphrase = getpass()
    print "repeat to be sure"
    confirm = getpass()
    if passphrase != confirm:
        print "passphrases do not match"
        return
    ################
    #  encryption  #
    ################
    file_path.write_bytes(encrypt(passphrase, "SUCC" + secret))
    print "password encrypted and stored"
