@echo off
path C:\TI;Z:\
if exist C:\POK.TXT del C:\POK.TXT
if exist C:\PFAIL.TXT del C:\PFAIL.TXT
cd C:\SRCP
gspa KANOMOV -h -l -v10 > C:\PKANOMOV.LOG
if errorlevel 1 goto failed
gspa SONYAMOV -h -l -v10 > C:\PSONYAMO.LOG
if errorlevel 1 goto failed
gspa KSCMD -h -l -v10 > C:\PKSCMD.LOG
if errorlevel 1 goto failed
gspa KANOART -h -l -v10 > C:\PKANOART.LOG
if errorlevel 1 goto failed
gspa SONYAART -h -l -v10 > C:\PSONYAAR.LOG
if errorlevel 1 goto failed
gspa KSANIM -h -l -v10 > C:\PKSANIM.LOG
if errorlevel 1 goto failed
gspa KANOANI -h -l -v10 > C:\PKANOANI.LOG
if errorlevel 1 goto failed
gspa SONYAANI -h -l -v10 > C:\PSONYAAN.LOG
if errorlevel 1 goto failed
gspa KSROOT -h -l -v10 > C:\PKSROOT.LOG
if errorlevel 1 goto failed
gspa KSUI -h -l -v10 > C:\PKSUI.LOG
if errorlevel 1 goto failed
gspa KSNAV -h -l -v10 > C:\PKSNAV.LOG
if errorlevel 1 goto failed
gspa KSPROJ -h -l -v10 > C:\PKSPROJ.LOG
if errorlevel 1 goto failed
gspa KSNUTART -h -l -v10 > C:\PNUTART.LOG
if errorlevel 1 goto failed
gspa KSIMART -h -l -v10 > C:\PIMART.LOG
if errorlevel 1 goto failed
gspa KSSHRED -h -l -v10 > C:\PSHRED.LOG
if errorlevel 1 goto failed
gspa KSPJROOT -h -l -v10 > C:\PKSPJRT.LOG
if errorlevel 1 goto failed
gspa KSPJANI -h -l -v10 > C:\PKSPJANI.LOG
if errorlevel 1 goto failed
gspa KSBLADE -h -l -v10 > C:\PKSBLADE.LOG
if errorlevel 1 goto failed
gspa KSBANI -h -l -v10 > C:\PKSBANI.LOG
if errorlevel 1 goto failed
gspa KSBIKE -h -l -v10 > C:\PKSBIKE.LOG
if errorlevel 1 goto failed
gspa KSBIANI -h -l -v10 > C:\PKSBIANI.LOG
if errorlevel 1 goto failed
gspa KSCHOKE -h -l -v10 > C:\PCHOKE.LOG
if errorlevel 1 goto failed
gspa KSCANI -h -l -v10 > C:\PCHANI.LOG
if errorlevel 1 goto failed
gspa KSLEG -h -l -v10 > C:\PLEG.LOG
if errorlevel 1 goto failed
gspa KSLANI -h -l -v10 > C:\PLEGANI.LOG
if errorlevel 1 goto failed
gspa KSPAIR -h -l -v10 > C:\PPAIR.LOG
if errorlevel 1 goto failed
gspa KSFART -h -l -v10 > C:\PFART.LOG
if errorlevel 1 goto failed
gspa KSFANI -h -l -v10 > C:\PFANI.LOG
if errorlevel 1 goto failed
gspa KSEXANI -h -l -v10 > C:\PEXANI.LOG
if errorlevel 1 goto failed
gspa KSFATAL -h -l -v10 > C:\PFATAL.LOG
if errorlevel 1 goto failed
gspa KSKSANI -h -l -v10 > C:\PKSANI.LOG
if errorlevel 1 goto failed
gspa KSKISS -h -l -v10 > C:\PKISS.LOG
if errorlevel 1 goto failed
gspa KSBUANI -h -l -v10 > C:\PBUANI.LOG
if errorlevel 1 goto failed
gspa KSBUBBLE -h -l -v10 > C:\PBUBBLE.LOG
if errorlevel 1 goto failed
gspa KSLAANI -h -l -v10 > C:\PLAANI.LOG
if errorlevel 1 goto failed
gspa KSREACT -h -l -v10 > C:\PREACT.LOG
if errorlevel 1 goto fail
gspa KSTRART -h -l -v10 > C:\PTRART.LOG
if errorlevel 1 goto failed
gspa KSDRAIN -h -l -v10 > C:\PDRAIN.LOG
if errorlevel 1 goto failed
gspa KSDRART -h -l -v10 > C:\PDRART.LOG
if errorlevel 1 goto failed
gspa KSDCART -h -l -v10 > C:\PDCART.LOG
if errorlevel 1 goto failed
gspa KSHDART -h -l -v10 > C:\PHDART.LOG
if errorlevel 1 goto failed
gspa KSBKART -h -l -v10 > C:\PBKART.LOG
if errorlevel 1 goto fail
gspa KSAI -h -l -v10 > C:\PAI.LOG
if errorlevel 1 goto fail
gspa KSTHANI -h -l -v10 > C:\PTHANI.LOG
if errorlevel 1 goto fail
gspa KSTHVIC -h -l -v10 > C:\PTHVIC.LOG
if errorlevel 1 goto fail
gspa KSTHROW -h -l -v10 > C:\PTHROW.LOG
if errorlevel 1 goto fail
gspa KSPITART -h -l -v10 > C:\PPITART.LOG
if errorlevel 1 goto fail
gspa KSFRIEND -h -l -v10 > C:\PFRIEND.LOG
if errorlevel 1 goto fail
gspa KSFRART -h -l -v10 > C:\PFRART.LOG
if errorlevel 1 goto fail
gspa KSNAMES -h -l -v10 > C:\PNAMES.LOG
if errorlevel 1 goto fail
gspa KSBABART -h -l -v10 > C:\PBABART.LOG
if errorlevel 1 goto fail
gspa KSLASER -h -l -v10 > C:\PLASER.LOG
if errorlevel 1 goto failed
gspa KSICEPAL -h -l -v10 > C:\PICEPAL.LOG
if errorlevel 1 goto failed
gspa KSARART -h -l -v10 > C:\PARART.LOG
if errorlevel 1 goto failed
gspa KSINFART -h -l -v10 > C:\PINFART.LOG
if errorlevel 1 goto failed
gspa KSINART -h -l -v10 > C:\PINART.LOG
if errorlevel 1 goto failed
gspa KSPLART -h -l -v10 > C:\PSPLART.LOG
if errorlevel 1 goto failed
gspa KSMOART -h -l -v10 > C:\PMOART.LOG
if errorlevel 1 goto failed
gspa KSENDART -h -l -v10 > C:\PENDART.LOG
if errorlevel 1 goto failed
gmake -m kombatw > C:\PBUILD.LOG
if errorlevel 1 goto failed
cd ROM
bigsrec < P.LRN > C:\PSPLIT.LOG
if errorlevel 1 goto failed
echo DONE > C:\POK.TXT
goto end
:failed
echo FAILED > C:\PFAIL.TXT
:end
exit
