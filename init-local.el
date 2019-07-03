;;; init-local.el ---- custom setting
;;; Commentary:
;;;

;;; Code:
(setq-default indent-tabs-mode nil)
(setq c-basic-offset 4)
(setq c-default-style "linux")
(setq default-tab-width 4)

(progn
  ;; Make whitespace-mode with very basic background coloring for whitespaces.
  ;; http://ergoemacs.org/emacs/whitespace-mode.html
  (setq whitespace-style (quote (face tabs newline tab-mark newline-mark )))

  ;; Make whitespace-mode and whitespace-newline-mode use “¶” for end of line char and “▷” for tab.
  (setq whitespace-display-mappings
        ;; all numbers are unicode codepoint in decimal. e.g. (insert-char 182 1)
        '(
          (newline-mark 10 [182 10]) ; LINE FEED,
          (tab-mark 9 [8677 9] [92 9])     ; tab
          )))
(global-whitespace-mode t)

(global-set-key (kbd "C-h") 'paredit-backward-delete)
(global-set-key (kbd "C-h") 'c-electric-backspace)

(global-set-key (kbd "M-h") 'paredit-backward-kill-word)

(global-set-key (kbd "M-H") 'kill-whole-line)

(require-package 'rust-mode)
(require-package 'counsel-gtags)
(add-hook 'c-mode-hook 'counsel-gtags-mode)
(add-hook 'c++-mode-hook 'counsel-gtags-mode)
(global-linum-mode t)
(with-eval-after-load 'counsel-gtags
  (define-key counsel-gtags-mode-map (kbd "M-t") 'counsel-gtags-find-definition)
  (define-key counsel-gtags-mode-map (kbd "M-r") 'counsel-gtags-find-reference)
  (define-key counsel-gtags-mode-map (kbd "M-s") 'counsel-gtags-find-symbol)
  (define-key counsel-gtags-mode-map (kbd "M-,") 'counsel-gtags-go-backward))

(setenv "GTAGSLIBPATH" (concat "/usr/include"
                               ":"
                               "/usr/src"
                               ":"
                               "/usr/local/include"))

(setenv "MAKEOBJDIRPREFIX" "/root/tmp/obj/")
(setq company-backends '((company-dabbrev-code company-gtags)))
(add-hook 'after-init-hook 'global-company-mode)

(provide 'init-local)
;;; init-local.el ends here
