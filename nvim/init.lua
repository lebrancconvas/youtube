-- basic functions -- 
vim.cmd("set number")
vim.cmd("set tabstop=4")
vim.cmd("set shiftwidth=4")
vim.cmd("set softtabstop=4")
vim.cmd("set mouse=")
vim.opt.fillchars = {eob = " "}
-- Lazy setup --
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
end
vim.opt.rtp:prepend(lazypath)

-- Plugins --
local plugins = {
	-- Lsp-zero --
	      -- Mason for lsp --
		  {"williamboman/mason.nvim",
		  "williamboman/mason-lspconfig.nvim",
		  "neovim/nvim-lspconfig"},					  
	{'VonHeikemen/lsp-zero.nvim', branch = 'v3.x'},
	{'neovim/nvim-lspconfig'},
	{'hrsh7th/cmp-nvim-lsp'},
	{'hrsh7th/nvim-cmp'},
	--{'L3MON4D3/LuaSnip'},

	-- Theme --
	{
  "cdmill/neomodern.nvim",
	lazy = false,
	priority = 1000,
	config = function()
    require("neomodern").setup({
    -- optional configuration here --
		style = "roseprime",
    })
    require("neomodern").load()
	end,
	},
	{
        'maxmx03/fluoromachine.nvim',
        config = function ()
         local fm = require 'fluoromachine'

         fm.setup {
            glow = true,
            theme = 'fluoromachine'
         }

		end
    },	
   {
	"folke/tokyonight.nvim",
	lazy = false,
	priority = 1000,
	opts = {},
	},

	--Lualine --
	{
    'nvim-lualine/lualine.nvim',
    dependencies = { 'nvim-tree/nvim-web-devicons' }
    },
	
	-- Telescope --
    {
    'nvim-telescope/telescope.nvim', tag = '0.1.6',
-- or                              , branch = '0.1.x',
      dependencies = { 'nvim-lua/plenary.nvim' }
    },
	
	-- Startup -- 
	{
  "startup-nvim/startup.nvim",
  requires = {"nvim-telescope/telescope.nvim", "nvim-lua/plenary.nvim"},
  config = function()
    require"startup".setup({theme = "dashboard"})
  end }, 
	
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
	{
    "nvim-treesitter/nvim-treesitter",
	build = ":TSUpdate",

	},

	-- terminal 
	{'akinsho/toggleterm.nvim', version = "*", config = true},


}


-- Setup --

require("lazy").setup(plugins, opts)

-- theme set up --
require("tokyonight").setup({
  -- use the night style
  style = "night",

  on_colors = function(colors)
  end
})

vim.cmd.colorscheme "neomodern"


-- lualine -- 

require('lualine').setup{
	options = { theme = 'tokyonight' }
}


--lsp-zero --

require('lsp-zero')
require('lspconfig').intelephense.setup({})

-- tree --

vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1
vim.opt.termguicolors = true
require("nvim-tree").setup()
vim.keymap.set('n', '<c-t>', ':NvimTreeFindFileToggle<CR>')
vim.keymap.set('n', '<c-n>', ':NvimTreeToggle<CR>')

-- treesitter --
require("nvim-treesitter.configs").setup({
          ensure_installed = { "c", "lua", "vim", "vimdoc", "query", "elixir", "heex", "javascript", "html" },
          sync_install = false,
          highlight = { enable = true },
          indent = { enable = true },  
        })

-- telescope & remaps --

local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, {})
vim.keymap.set('n', '<leader>fg', builtin.live_grep, {})
vim.keymap.set('n', '<leader>fb', builtin.buffers, {})
vim.keymap.set('n', '<leader>fh', builtin.help_tags, {})

-- terminal rempas
vim.keymap.set('n', '<c-`>', ':ToggleTerm size=20<CR>')
-- lsp set up -- 
	-- mason set up 
	require("mason").setup({
    ui = {
        icons = {
            package_installed = "✓",
            package_pending = "➜",
            package_uninstalled = "✗"
        }
    }
})
	require("mason-lspconfig").setup {
    ensure_installed = { "lua_ls", "rust_analyzer" },
}


-- cmp (autocompletion) setup 

local cmp = require('cmp')
local cmp_format = require('lsp-zero').cmp_format({details = true})

cmp.setup({
  window = {
      completion = cmp.config.window.bordered(),
      documentation = cmp.config.window.bordered(),
  },
  mapping = cmp.mapping.preset.insert({
    -- confirm completion
    ['<Tab>'] = cmp.mapping.confirm({select = true}),
  }),
	sources = cmp.config.sources({
      { name = 'nvim_lsp' },
      --{ name = 'vsnip' }, -- For vsnip users.
	  --{ name = 'luasnip' }, -- For luasnip users.
      -- { name = 'ultisnips' }, -- For ultisnips users.
      -- { name = 'snippy' }, -- For snippy users.
    }, {
      { name = 'buffer' },
    })
})

local lsp_zero = require('lsp-zero')

lsp_zero.on_attach(function(client, bufnr)
  -- see :help lsp-zero-keybindings
  -- to learn the available actions
  lsp_zero.default_keymaps({buffer = bufnr})
end)

-- to learn how to use mason.nvim
-- read this: https://github.com/VonHeikemen/lsp-zero.nvim/blob/v3.x/doc/md/guide/integrate-with-mason-nvim.md
require('mason').setup({})
require('mason-lspconfig').setup({
  ensure_installed = {},
  handlers = {
    function(server_name)
      require('lspconfig')[server_name].setup({})
    end,
  },
})
