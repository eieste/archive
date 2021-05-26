:set number


call plug#begin('~/.vim/plugged')

Plug 'davidhalter/jedi-vim'
Plug 'itchyny/lightline.vim'
Plug 'preservim/nerdtree'
Plug 'dense-analysis/ale'

Plug 'airblade/vim-gitgutter'
Plug 'speshak/vim-cfn'
Plug 'https://github.com/m-kat/aws-vim'
Plug 'preservim/nerdtree'
Plug 'xavierchow/vim-swagger-preview'

Plug 'Shougo/denite.nvim'
Plug 'Quramy/vison'


Plug 'avakhov/vim-yaml'


call plug#end()



let g:lightline = {
      \ 'colorscheme': 'solarized',
      \ }


set mouse=a

function! StartUp()
    if !argc() && !exists("s:std_in")
        NERDTree
    end
    if argc() && isdirectory(argv()[0]) && !exists("s:std_in")
        exe 'NERDTree' argv()[0]
        wincmd p
        ene
    end
endfunction

autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * call StartUp()


map <C-n> :NERDTreeToggle<CR>

autocmd FileType json setlocal completeopt+=menu,preview
