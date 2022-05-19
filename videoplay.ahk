
result := MsgBox("播放暂停，是否激活",, "Y/N T2")
    
if (result = "No"){
    return
}

if WinExist("ahk_class" "IEFrame"){

    WinActivate
    Sleep 200
    
    MouseClick "left", 140, 90
    Sleep 200

    ImageFile := "*32 D:\button2.png"
    try{
	if ImageSearch(&OutputVarX, &OutputVarY, 600, 500, 1200, 800, ImageFile){

	    MouseClick "left", OutputVarX + 20, OutputVarY + 5
    	    Sleep 200

	    MouseClick "left", 1720, 960
    	    Sleep 200

	    MouseClick "left", 1720, 890
    	    Sleep 200
        }
    	else{
    	    MsgBox("播放结束",, "Y/N T2")
        }
    }
}
