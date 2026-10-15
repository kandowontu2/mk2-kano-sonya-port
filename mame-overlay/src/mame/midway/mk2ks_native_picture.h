// license:BSD-3-Clause
// Original MK3 FF929660/FF9298C0/FF92A3B0/FF92A6E0 picture codec.
// Initialization only: gameplay retains the original MKII picture decoder.
#ifndef MAME_MIDWAY_MK2KS_NATIVE_PICTURE_H
#define MAME_MIDWAY_MK2KS_NATIVE_PICTURE_H
#include <algorithm>
#include <array>
#include <cstdint>
#include <stdexcept>
#include <vector>
namespace mk2ks_picture {
struct picture
{
	unsigned width, height;
	std::vector<uint16_t> palette;
	std::vector<uint8_t> pixels; // Original bottom-up row order.
};
class reader
{
public:
	reader(uint8_t const *data, unsigned bytes) : m_data(data), m_bytes(bytes) { }
	unsigned read(unsigned count)
	{
		if (m_position + count > uint64_t(m_bytes) * 8)
			throw std::runtime_error("truncated native picture");
		unsigned value = 0;
		for (unsigned bit = 0; bit < count; bit++, m_position++)
			value |= unsigned((m_data[m_position / 8] >> (m_position & 7)) & 1) << bit;
		return value;
	}
private:
	uint8_t const *m_data;
	unsigned m_bytes;
	uint64_t m_position = 0;
};
struct code { unsigned length, bits, symbol; };
using book = std::array<code, 64>;
inline book read_book(reader &bits)
{
	unsigned const groups = bits.read(8) + 1;
	std::array<unsigned, 64> lengths{}, order{};
	unsigned symbols = 0;
	for (unsigned group = 0; group < groups; group++)
	{
		unsigned const packed = bits.read(8), repeat = (packed >> 4) + 1;
		if (symbols + repeat > 64) throw std::runtime_error("native codebook has too many symbols");
		for (unsigned n = 0; n < repeat; n++) lengths[symbols++] = (packed & 15) + 1;
	}
	if (symbols != 64) throw std::runtime_error("native codebook must contain 64 symbols");
	for (unsigned n = 0; n < 64; n++) order[n] = n;
	std::sort(order.begin(), order.end(), [&lengths](unsigned a, unsigned b)
		{ return lengths[a] != lengths[b] ? lengths[a] < lengths[b] : a < b; });
	book result{};
	unsigned prefix = 0, step = 0, previous = 0;
	for (unsigned n = 0; n < 64; n++)
	{
		unsigned const symbol = order[63 - n], length = lengths[symbol];
		prefix += step;
		if (prefix >= 65536) throw std::runtime_error("native codebook prefix overflow");
		if (previous != length) { step = 1U << (16 - length); previous = length; }
		unsigned reverse = 0;
		for (unsigned b = 0; b < 16; b++) reverse |= ((prefix >> b) & 1) << (15 - b);
		reverse &= (1U << length) - 1;
		for (unsigned prior = 0; prior < n; prior++)
			if (result[prior].length == length && result[prior].bits == reverse)
				throw std::runtime_error("ambiguous native codebook");
		result[n] = { length, reverse, symbol };
	}
	return result;
}
inline unsigned read_symbol(reader &bits, book const &codes)
{
	unsigned prefix = 0;
	for (unsigned length = 1; length <= 16; length++)
	{
		prefix |= bits.read(1) << (length - 1);
		for (auto const &entry : codes)
			if (entry.length == length && entry.bits == prefix) return entry.symbol;
	}
	throw std::runtime_error("invalid native Huffman symbol");
}
inline picture decode(uint8_t const *data, unsigned bytes)
{
	reader bits(data, bytes);
	picture result;
	result.width = bits.read(16); result.height = bits.read(16);
	unsigned const frames = bits.read(16), colors = bits.read(16);
	if (!result.width || result.width > 1024 || !result.height || result.height > 1024 ||
		frames != 1 || !colors || colors > 256)
		throw std::runtime_error("unsupported native picture header");
	for (unsigned n = 0; n < colors; n++) result.palette.push_back(bits.read(16));
	book const lengths = read_book(bits), distances = read_book(bits);
	unsigned const target = result.width * result.height;
	result.pixels.reserve(target);
	while (result.pixels.size() < target)
	{
		if (bits.read(1)) result.pixels.push_back(bits.read(8));
		else
		{
			unsigned const low = bits.read(6);
			unsigned const distance = (low | (read_symbol(bits, distances) << 6)) + 1;
			unsigned run = read_symbol(bits, lengths);
			if (run == 63) run += bits.read(8);
			run += 2;
			if (result.pixels.size() + run > target)
				throw std::runtime_error("native copy exceeds picture dimensions");
			for (unsigned n = 0; n < run; n++)
				result.pixels.push_back(result.pixels.size() >= distance ?
					result.pixels[result.pixels.size() - distance] : 0);
		}
	}
	for (uint8_t pixel : result.pixels)
		if (pixel >= colors) throw std::runtime_error("native pixel exceeds palette");
	return result;
}
} // namespace mk2ks_picture
#endif
