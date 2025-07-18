// CButton.h

#ifndef _CButton_h
#define _CButton_h

 
// Pointer to event handling methods
extern "C" {
    typedef void (*ButtonEventHandler)(void);
}
// void my_singeClick_function(){}

class CButton{
    public:
        CButton(int port);
        void attachSingleClick(ButtonEventHandler method){singleClick = method;};
        void attachDoubleClick(ButtonEventHandler method){doubleClick = method;};
        void attachLongPress(ButtonEventHandler method){longPress = method;};

        void tick();

    private:
        ButtonEventHandler singleClick = NULL;
        ButtonEventHandler doubleClick = NULL;
        ButtonEventHandler longPress = NULL;

        gpio_num_t pinNum;  // pohrana broja GPIO pina na kojem je tipka spojena

        const char *LogName = "CButton";    // iz kojeg dijela programa dolazi log
        bool pressBeforeBtn = false;    // razlikovanje single i double klika
        bool prevTick = false;  // prosli ciklus obradio tipku
        int64_t lastPressTime = 0;  // pohrana vremena pritiska
        bool handleEvent = false;   // kontrola obrade dogadaja (unutar ciklusa)
};


#endif