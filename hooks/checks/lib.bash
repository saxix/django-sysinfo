#!/usr/bin/env bash

## Colors
RED=`printf '\033[1;31m'`
GREEN=`printf '\033[1;32m'`
WHITE=`printf '\033[1;37m'`
GREY=`printf '\033[1;36m'`
NC='\033[0m' # No Color

#
## Icons
CHECK=`printf ${GREEN}'✔'${NC}`
CROSS=`printf ${RED}'✘'${NC}`

REPO_DIR=$(git rev-parse --show-toplevel 2> /dev/null)
DOT_GIT_DIR=$(git rev-parse --git-dir)
if [ "$DOT_GIT_DIR" = ".git" ]; then
	DOT_GIT_DIR="$REPO_DIR"/"$DOT_GIT_DIR"
fi
HOOKS_CHECK_DIR="$DOT_GIT_DIR"/hooks/checks

AVH_MAJOR=""
AVH_MINOR=""
AVH_PATCH_LEVEL=""
AVH_PRE_RELEASE=""
AVH_VERSION=""
#
#
## Modules directory
#HOOKS_MODULES_DIR="$HOOKS_DIR"/modules
#
#REPO_DIR="$(git rev-parse --show-toplevel 2>/dev/null)"
#if [ ! -f "$REPO_DIR"/.git/hooks_config ]; then
#	echo "\n${CROSS}${RED} Missing file "$REPO_DIR"/.git/hooks_config"
#	exit 127
#fi
#. "$REPO_DIR"/.git/hooks_config
#
#type _update_version >/dev/null 2>&1;
#if [ $? -eq 127 ]; then
#	echo "\n${CROSS}${RED} Missing function _update_version!\nThis function should be declared in "$REPO_DIR"/.git/hooks_config"
#	exit 127
#fi
#
#gitflow_update_version() {
#	if [ -n "$2" ]; then
#		MSG="$2"
#	else
#		MSG="Version bump $1"
#	fi
#	_update_version $1
#	git commit -a -m "$MSG"
#}
#
#gitflow_set_major_minor() {
#	local TEMP_VERSION=$1
#	AVH_MAJOR=$(echo "$TEMP_VERSION" | cut -f1 -d".")
#	if $(gitflow_contains "$TEMP_VERSION" "."); then
#		TEMP_VERSION=$(echo ${TEMP_VERSION#*.})
#		AVH_MINOR=$(echo "$TEMP_VERSION" | cut -f1 -d"."|cut -f1 -d"-")
#		if [ -z $AVH_MINOR ]; then
#			AVH_MINOR=0
#			AVH_PATCH_LEVEL=0
#		else
#			if $(gitflow_contains "$TEMP_VERSION" "."); then
#				TEMP_VERSION=$(echo ${TEMP_VERSION#*.})
#				AVH_PATCH_LEVEL=$(echo "$TEMP_VERSION" | cut -f1 -d"."|cut -f1 -d"-")
#				[ -z $AVH_PATCH_LEVEL ] && AVH_PATCH_LEVEL=0
#			else
#				AVH_PATCH_LEVEL=0
#			fi
#		fi
#	else
#		AVH_MINOR=0
#		AVH_PATCH_LEVEL=0
#	fi
#}
#
#gitflow_build_version() {
#	AVH_VERSION=$AVH_MAJOR.$AVH_MINOR.$AVH_PATCH_LEVEL
#	[ -n AVH_PRE_RELEASE ] && AVH_VERSION=$AVH_VERSION$AVH_PRE_RELEASE
#}
#
##
## Set the pre-release, it counts all commits but not the one in master
##
#gitflow_set_dev_release() {
#	AVH_PRE_RELEASE=-dev.$(git rev-list --count HEAD ^"$MASTER_BRANCH")
#}
#
##
## Set the rc-release, it counts all commits but not the one in master
##
#gitflow_set_rc_release() {
#	local RC_LEVEL=$(echo "$1" | cut -f2 -d"-"|cut -f2 -d".")
#	RC_LEVEL=$(($RC_LEVEL+1))
#	AVH_PRE_RELEASE=-rc.$RC_LEVEL
#}
#
#gitflow_get_current_version() {
#	CURRENT_VERSION=$(grep -m1 "GITFLOW_VERSION=" $ROOTDIR/git-flow-version | cut -f2 -d"=")
#	echo "$CURRENT_VERSION"
#}
#
##
# Create an up to date AUTHORS file
#
gitflow_update_authors() {

#    ROOTDIR=$(git rev-parse --show-toplevel)
    AUTHORS=$(mktemp -t wfpoauth)
    # Create an up to date AUTHORS file
    echo "Authors
    "> $AUTHORS
    git shortlog -ns --no-merges | cut -f2 >> $AUTHORS

    echo "

This file is auto generated, any changes will be lost." >> $AUTHORS

    # Check if the new file is different
    # If it's not there is no need to copy it and commit
    diff $AUTHORS $REPO_DIR/AUTHORS > /dev/null 2>&1
    DIFF=$?
    if [ $DIFF -ne 0 ]; then
        cp $AUTHORS $REPO_DIR/AUTHORS
        git commit AUTHORS -m "Update of the contributers." --no-verify
    fi
    # Clean up
    rm  $AUTHORS
    gitflow_ok "AUTHORS updated ($REPO_DIR/AUTHORS)"
}

#
#
# String contains function
# $1 haystack
# $2 Needle
#
gitflow_contains() {
	local return

	case $1 in
		*$2*)
			return=0
			;;
		*)
			return=1
			;;
	esac
	return $return
}

gitflow_fail() {
	echo -e "\t"${CROSS} ${GREY}$1${NC}
}
#
gitflow_ok() {
	echo -e "\t"${CHECK} ${GREY}$1${NC}
}

h1() {
	echo -e "\n${NC}$1 ...\n"
}


gitflow_error() {
	echo -e "\n${RED}$1 ...\n"
}

gitflow_success() {
	echo -e "\n${CHECK} ${GREEN}$1 ...${NC}\n"
}

#
## Function to get a list of files that will be committed by extension
## you can for example do "$(commit_files js css)" to get a list of js and css files that will be committed
gitflow_commit_files() {

	if [ $# -eq 0 ] ; then
	    echo $(git diff-index --name-only --diff-filter=ACM --cached HEAD --)
	    exit 0
	fi

	extensions=''
	for extension in "$@"
	do
		extensions="${extensions}(${extension})|"
	done
	regex="\.(${extensions%?})$"
	echo $(git diff-index --name-only --diff-filter=ACM --cached HEAD -- | grep -E "$regex")
}

#gitflow_count_commit_files() {
#	echo $(gitflow_commit_files $@) | wc -w | tr -d ' '
#}
#
#gitflow_validInt() {
#	local _return
#
#	[ -n "$1" ] || return 1
#	_int="$1"
#	case "${_int}" in
#		*[!0-9]*) _return=1 ;;
#		*) _return=0 ;;
#	esac
#	return $_return
#}
