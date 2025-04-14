use strict;
use warnings;
use Tk;

# Создаем главное окно
my $main_window = MainWindow->new;
$main_window->title("Simple Perl Window");

# Добавляем кнопку
my $button = $main_window->Button(
    -text    => "Click Me!",
    -command => sub { print "Button clicked!\n"; }
)->pack;

# Запускаем главный цикл обработки событий
MainLoop;
