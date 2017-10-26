#!/usr/bin/perl

# ---------------------------------------------------------------------------------------------------
#
# usage:
# example:
#
# ---------------------------------------------------------------------------------------------------
use Getopt::Long;
use File::Glob ':globally';
use File::Find;

@DIRLIST = ('.');

#default name for input file
my $FileName = "targo_cleaner.txt";

GetOptions('FileName=s'  => \$FileName,
	   'OutputFileName=s'  => \$FileNameOut);
#default name for output file
my $FileNameOut = ${FileName}.".out";

my $repeat_counter = 0;
my $bucket = 0;
my $AddrBucket = 0;
my $min_bucket = -1;
my $max_bucket = 0;
my $time_interval = 100000000; # 0.1 second
my %BTransfers;
my %DBGTransfers;
my %RepeatCounter;
my $DRAM_start  = 0x80000000;
my $HPRAM_start = 0xBE000000;
my $LPRAM_start = 0xBE800000;
my $ROM_start   = 0xBEFE0000;

push (@ListOfSources, $FileName);

# main processing loop for files
foreach $file (@ListOfSources) {
  # initialize values
  open (MYFILE, $file) || die "Couldn't open $file \n";
  LOOP:while(<MYFILE>) {
    chomp;
    s/^\s+//;
    @elements = split(/,/, $_);
    if (/^201\d-(\d\d)/) { 
      my $currentMonth = $1;
      # print "Debug: $1\n";
      if ($elements[2] =~ /^[-]*\d+\.\d+/) {
	# print ".";
      }
      else {
        print "weird amount $elements[2]\n";
      };
      $sum += $elements[2];
      if ($currentMonth != $rememberMonth) {
	printf "DEBUG: sum on $elements[0] is %.2f\n",$sum;
      };
      $rememberMonth = $currentMonth;
    };
  };
  close(MYFILE);
};

