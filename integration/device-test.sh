#!/usr/bin/env bash
source $(dirname ${BASH_SOURCE[0]})/assert.sh

PROG=`realpath $1`
UNITSNUM=${UNITSNUM:-3}
MNTDIR=`mktemp -d`

cleanup() {
    echo Remove mountpoint $MNTDIR
    fusermount -u $MNTDIR || (echo "Trying sudo..."; sudo fusermount -u $MNTDIR && echo DONE)
    rmdir $MNTDIR
    exit $RESULT
}

trap cleanup EXIT INT

# Test section

echo Mount $MNTDIR by $PROG
assert $PROG --units=$UNITSNUM $MNTDIR

assert echo 0 '>' $MNTDIR/ctrl
assert printf 0 '|' diff - $MNTDIR/ctrl
assert echo 0 '>' $MNTDIR/ctrl
assert echo 1 '>' $MNTDIR/ctrl
assert echo 2 '>' $MNTDIR/ctrl
assert printf '0\\n1\\n2' '|' diff - $MNTDIR/ctrl

assert echo 123 '>' $MNTDIR/unit0/lram
assert echo 321 '>' $MNTDIR/unit0/pram
assert echo 123 '|' diff - $MNTDIR/unit0/lram
assert echo 321 '|' diff - $MNTDIR/unit0/pram

# End of test section

if [[ $RESULT -ne 0 ]]; then
    printf "\n****************FAILED****************\n"
else
    printf "\nAll is fine!\n"
fi

exit $RESULT
