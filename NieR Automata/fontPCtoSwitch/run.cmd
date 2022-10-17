python dat_unpacker.py %1.dat
python dat_unpacker.py %1.dtt
python wtb_unpacker.py "%1\%1"
python toASTC.py "%1\%1"
python toWTB.py %1
copy /b %1\%1.ftb new\%1.ftb
copy /b %1\%1.ktb new\%1.ktb
rmdir /s /q %1
ren new %1
python dat_repacker.py %1.dat
python dat_repacker.py %1.dtt
pause