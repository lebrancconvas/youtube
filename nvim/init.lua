vim.cmd("set number")
vim.cmd("set tabstop=4")
vim.cmd("set softtabstop=4")
vim.cmd("set shiftwidth=4")
vim.cmd("set mouse=")
vim.opt.fillchars = {eob = " "}

-- Lazy set up 
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
      { out, "WarningMsg" },
      { "\nPress any key to exit..." },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end
vim.opt.rtp:prepend(lazypath)

-- Plugins 

-- tokyonight

local plugins = {
{
  "folke/tokyonight.nvim",
  lazy = false,
  priority = 1000,
  opts = {},
},


-- lualine 
{
    'nvim-lualine/lualine.nvim',
    dependencies = { 'nvim-tree/nvim-web-devicons' }
},

-- telescope 
{
    'nvim-telescope/telescope.nvim', tag = '0.1.8',
    dependencies = { 'nvim-lua/plenary.nvim' }
},



-- treesitter 
{
	"nvim-treesitter/nvim-treesitter",
	build = ":TSUpdate",
},

-- nvim tree
{
  "nvim-tree/nvim-tree.lua",
  version = "*",
  lazy = false,
  dependencies = {
    "nvim-tree/nvim-web-devicons",
  },
  config = function()
    require("nvim-tree").setup {}
  end,
},


-- lsp & mason
{"williamboman/mason.nvim"},
{"williamboman/mason-lspconfig.nvim"},
{"neovim/nvim-lspconfig"},
{'VonHeikemen/lsp-zero.nvim', branch = 'v3.x'},
{'neovim/nvim-lspconfig'},
{'hrsh7th/cmp-nvim-lsp'},
{'hrsh7th/nvim-cmp'},
{'L3MON4D3/LuaSnip'},

--terminal 
{'akinsho/toggleterm.nvim', version = "*", config = true},

}

-- Setup 
 require("lazy").setup(plugins, opts)

-- tokyonight
require("tokyonight").setup({
	style="night",
	on_colors = function(colors)
	end

})
vim.cmd.colorscheme "tokyonight"

--	lualine 
require("lualine").setup{
	options = {theme = "tokyonight" }
}

-- nvim tree
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1
vim.opt.termguicolors = true
require("nvim-tree").setup()
vim.keymap.set("n", '<c-t>', ':NvimTreeFindFileToggle<CR>')
vim.keymap.set("n", '<c-n>', ':NvimTreeToggle<CR>')


-- treesitter 
require("nvim-treesitter.configs").setup({
	ensure_installed = { "c", "lua", "vim", "vimdoc", "query", "rust"},
	sync_install = false,
	highlight = { enable = true },
	indent = {enable = true},
})

-- telescope 
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, {})
vim.keymap.set('n', '<leader>fg', builtin.live_grep, {})
vim.keymap.set('n', '<leader>fb', builtin.buffers, {})
vim.keymap.set('n', '<leader>fh', builtin.help_tags, {})

--cmp
local cmp = require("cmp")
local cmp_format = require('lsp-zero').cmp_format({details = true})
cmp.setup({
    mapping = cmp.mapping.preset.insert({
      ['<Tab>'] = cmp.mapping.confirm({select = true}),
    }),
    sources = cmp.config.sources({
      { name = 'nvim_lsp' },
      { name = 'vsnip' }, -- For vsnip users.
    }, {
      { name = 'buffer' },
    })
  })

-- lsp
local lsp_zero = require('lsp-zero')

lsp_zero.on_attach(function(client, bufnr)
  lsp_zero.default_keymaps({buffer = bufnr})
end)

--mason
require('mason').setup({})
require('mason-lspconfig').setup({
  ensure_installed = {'rust_analyzer', 'clangd', 'pyright'},
  handlers = {
    function(server_name)
      require('lspconfig')[server_name].setup({})
    end,
  },
})

--terminads
vim.keymap.set('n', '<c-`>', ':ToggleTerm<CR>')
require'toggleterm'.setup {
	shade_terminals = false,
	direction = 'float',
	border = 'curved',
	persist_mode = true,
	shell = vim.o.shell,
	float_opts = {
		border = 'curved', 
		width = 150,
		height = 30,
	},
}


function _G.set_terminal_keymaps()
  local opts = {buffer = 0}
  vim.keymap.set('t', '<esc>', [[<C-\><C-n>]], opts)
  vim.keymap.set('t', 'jk', [[<C-\><C-n>]], opts)
  vim.keymap.set('t', '<C-h>', [[<Cmd>wincmd h<CR>]], opts)
  vim.keymap.set('t', '<C-j>', [[<Cmd>wincmd j<CR>]], opts)
  vim.keymap.set('t', '<C-k>', [[<Cmd>wincmd k<CR>]], opts)
  vim.keymap.set('t', '<C-l>', [[<Cmd>wincmd l<CR>]], opts)
  vim.keymap.set('t', '<C-w>', [[<C-\><C-n><C-w>]], opts)
end
