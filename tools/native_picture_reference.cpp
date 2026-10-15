// Standalone test adapter for the actual production decoder (binary stdin/stdout).
#include "../mame-mkp/src/mame/midway/mk2ks_native_picture.h"
#include <iostream>
#include <iterator>
#ifdef _WIN32
#include <fcntl.h>
#include <io.h>
#endif
int main()
{
#ifdef _WIN32
	_setmode(_fileno(stdin), _O_BINARY);
	_setmode(_fileno(stdout), _O_BINARY);
#endif
	try
	{
		std::vector<uint8_t> source(std::istreambuf_iterator<char>(std::cin), {});
		auto const photo = mk2ks_picture::decode(source.data(), source.size());
		uint32_t const header[3] = { photo.width, photo.height, uint32_t(photo.palette.size()) };
		std::cout.write(reinterpret_cast<char const *>(header), sizeof(header));
		std::cout.write(reinterpret_cast<char const *>(photo.palette.data()), photo.palette.size() * 2);
		std::cout.write(reinterpret_cast<char const *>(photo.pixels.data()), photo.pixels.size());
	}
	catch (std::exception const &error) { std::cerr << error.what(); return 2; }
	return 0;
}
