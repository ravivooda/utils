#!/bin/bash
FOLDERS=()

CURRDIR=./

function replacer {
    FILERR=$1
    TEMPFILE=output.txt
    sed 's/\/\/Log.d/Log.d/g' $FILERR > $TEMPFILE && mv $TEMPFILE $FILERR
    sed 's/Log.d/\/\/Log.d/g' $FILERR > $TEMPFILE && mv $TEMPFILE $FILERR
}

function pushFolders {
    DIR=$1
    #    if [ -d $DIR ]; then
    #	echo -e "This is not a directory: $DIR"
    #	return
    #    fi
    #echo -e "Searching now in $DIR"
    for f in $( ls $DIR ); do
	DIRPATH=${DIR%%/}/$f
	if [ -d $DIRPATH ]; then
	    FOLDERS+=($DIRPATH)
	else
	    echo -e "This is a file. Should check for logging $DIRPATH"
	    replacer $DIRPATH
	    #exit
	fi
    done
}

ARGCOUNT=$#
if [ $ARGCOUNT -eq 0 ]; then
    echo -e "You input 0 arguments.\n\tArgument 1: relative path to directory.\n\tArgument 2: Anything you want"
    exit
fi

ROOTDIR=$1
if [ -d $ROOTDIR ]; then
    echo -e "Searching for Logging in directory $ROOTDIR"
    CURRDIR=$ROOTDIR
    FOLDERS+=($CURRDIR)
    while [ ${#FOLDERS[@]} -gt 0 ]; do
	pushFolders $CURRDIR
	FOLDERS=("${FOLDERS[@]:1}") #removing the first element
	CURRDIR=${FOLDERS[0]}
    done
else
    echo -e "No such directory $ROOTDIR"
fi
