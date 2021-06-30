#include <iostream>
#include <stdio.h>


size_t LZSS_Decode(void* _src, void* _dst)
{
    unsigned int uncompressed_size; // w20
    int compressed_size; // w22
    int compressed_flag; // w24
    uint8_t* v5; // x19
    int v6; // w25
    int v7; // w23
    char* data_pointer; // x26
    __int64 v9; // x8
    int v10; // w9
    int v11; // w9
    signed __int64 v12; // x25
    int v13; // w8
    int v14; // w21

    uncompressed_size = *(uint32_t*)_src;
    if (_dst)
    {
        compressed_size = *((uint32_t*)_src + 1) - 12;
        if (compressed_size >= 1)
        {
            compressed_flag = *((uint32_t*)_src + 2);
            v5 = (uint8_t*)_dst;
            v6 = 0;
            v7 = 0;
            data_pointer = (char*)_src + 12;
            while (1)
            {
                v9 = v6;
                v10 = (unsigned __int8)data_pointer[v6];
                if (compressed_flag != v10)
                    break;
                ++v6;
                v11 = (unsigned __int8)data_pointer[v9 + 1];
                if (compressed_flag == v11)
                {
                    v5[v7] = compressed_flag;
                LABEL_8:
                    ++v6;
                    ++v7;
                    if (v6 >= compressed_size)
                        return uncompressed_size;
                }
                else
                {
                    v12 = v9 + 2;
                    v13 = v7 - v11;
                    v14 = (unsigned __int8)data_pointer[v12];
                    if (compressed_flag < v11)
                        ++v13;
                    memcpy(&v5[v7], &v5[v13], (unsigned __int8)data_pointer[v12]);
                    v6 = v12 + 1;
                    v7 += v14;
                    if (v6 >= compressed_size)
                        return uncompressed_size;
                }
            }
            v5[v7] = v10;
            goto LABEL_8;
        }
    }
    return uncompressed_size;
}



int main(int argc, char* argv[])
{
    FILE* file = new FILE;
    std::string var1 = argv[1];
    std::string var2 = argv[2];
    fopen_s(&file, var1.c_str(), "rb");
    uint32_t uncompressed_size = 0;
    uint32_t compressed_size = 0;
    fread(&uncompressed_size, 1, 4, file);
    fread(&compressed_size, 1, 4, file);
    void* data = (void*)malloc(compressed_size);
    fseek(file, 0, 0);
    fread(data, 1, compressed_size, file);
    void* uncompressed = (void*)malloc(uncompressed_size);
    size_t size = LZSS_Decode(data, uncompressed);
    FILE* new_file = new FILE;
    fopen_s(&new_file, var2.c_str(), "wb");
    fwrite(uncompressed, size, 1, new_file);
    std::cout << "Hello World!\n";
}
