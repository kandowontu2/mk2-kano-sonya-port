	// SHANG_OWNED_REACTION_BEGIN
	// Native main56 starts with an owned recoil, then four token4 shake
	// records inherited Liu's external FF9D7CB0 composite. Keep the recoil,
	// every token, separator and packed X/Y parameter. Use the actual victim's
	// owned main40 dizzy composite during the four subsequent shake records.
	// This only repairs the lead-in. The separate FF9D7770 shrink-animation
	// and FF9D8D70 palette tables must also be extended before this is built.
	uint8_t *const shang_owned_data = memregion("mk3data")->base();
	constexpr unsigned shang_owned_roots[2] = { 0x100000, 0x104000 };
	constexpr uint32_t shang_owned_scripts[2] = { 0xff00b070, 0xff02b070 };
	constexpr uint32_t shang_owned_recoils[2] = { 0xff013300, 0xff033420 };
	constexpr uint32_t shang_owned_dizzies[2] = { 0xff011f60, 0xff0320c0 };
	constexpr unsigned shang_owned_cells[4] = { 24, 36, 48, 60 };
	constexpr uint32_t shang_owned_xy[4] = { 0x001afff6, 0xfff80013, 0xffec0008, 0 };
	if (memregion("mk3data")->bytes() != 0x200000)
		fatalerror("MK2KS: unsupported owned Shang victim data size");
	// Validate both complete scripts and both typed composites BEFORE writing
	// either character. Do not truncate the renderer or replace an actor ID.
	for (unsigned fighter = 0; fighter < 2; fighter++)
	{
		unsigned const root = shang_owned_roots[fighter];
		uint32_t const script = donor32(root + 56 * 4);
		uint32_t const dizzy = donor32(root + 40 * 4);
		if (script != shang_owned_scripts[fighter] ||
			dizzy < 0xfe800000U || dizzy >= 0xff800000U || (dizzy & 15))
			fatalerror("MK2KS: owned Shang reaction root changed");
		unsigned const at = (script - 0xfe800000U) / 8;
		uint32_t const group = donor32((dizzy - 0xfe800000U) / 8);
		if (group != shang_owned_dizzies[fighter] || donor32(at) != 4 ||
			donor32(at + 4) != 0xffedffb8 ||
			donor32(at + 8) != shang_owned_recoils[fighter] || donor32(at + 12))
			fatalerror("MK2KS: owned Shang initial recoil changed");
		for (unsigned phase = 0; phase < 4; phase++)
		{
			unsigned const cell = at + shang_owned_cells[phase];
			if (donor32(cell - 8) != 4 || donor32(cell - 4) != shang_owned_xy[phase] ||
				donor32(cell) != 0xff9d7cb0)
				fatalerror("MK2KS: original Shang lead-in grammar changed");
		}
		unsigned parts = 0;
		for (; parts < 8; parts++)
		{
			uint32_t const frame = donor32((group - 0xfe800000U) / 8 + parts * 4);
			if (!frame) break;
			if (frame < 0xfe800000U || frame >= 0xff7fff00U || (frame & 15))
				fatalerror("MK2KS: owned dizzy composite is not a descriptor list");
			unsigned const descriptor = (frame - 0xfe800000U) / 8;
			unsigned const dimensions = donor32(descriptor);
			if (!(dimensions & 0xffff) || (dimensions & 0xffff) > 256 ||
				!(dimensions >> 16) || (dimensions >> 16) > 256 ||
				((donor32(descriptor + 12) >> 12) & 7) != 6)
				fatalerror("MK2KS: owned dizzy bitmap format changed");
		}
		if (!parts || parts == 8)
			fatalerror("MK2KS: owned dizzy composite does not terminate");
	}
	for (unsigned fighter = 0; fighter < 2; fighter++)
		for (unsigned cell : shang_owned_cells)
		{
			unsigned const at = (shang_owned_scripts[fighter] - 0xfe800000U) / 8 + cell;
			uint32_t const group = shang_owned_dizzies[fighter];
			shang_owned_data[at] = group;
			shang_owned_data[at + 1] = group >> 8;
			shang_owned_data[at + 2] = group >> 16;
			shang_owned_data[at + 3] = group >> 24;
		}
	// SHANG_OWNED_REACTION_END
