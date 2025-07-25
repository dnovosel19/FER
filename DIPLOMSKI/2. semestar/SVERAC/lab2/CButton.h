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

        void tick();

    private:
        ButtonEventHandler singleClick = NULL;

        gpio_num_t m_pinNumber;
        const char *LogName = "CButton";
        bool buttonPressed = false;
};


#endif