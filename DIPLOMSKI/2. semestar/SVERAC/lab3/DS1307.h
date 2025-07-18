#ifndef _DS1307_h
#define _DS1307_h

class DS1307 {
    public:
        DS1307(unsigned char address, int SDA_pin, int SCL_pin);
        static uint8_t intToBCD(uint8_t num);
        static uint8_t BCDToInt(uint8_t num);
        void setTime(uint8_t sec, uint8_t min, uint8_t hour, uint8_t wday, uint8_t day, uint8_t mon, int year);
        void readValue();
        void setSpecific(int inputValue, uint8_t position);
        void readRegister(int reg);

    private:
        unsigned char address;
};

#endif