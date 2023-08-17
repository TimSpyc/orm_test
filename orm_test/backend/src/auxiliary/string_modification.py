import sys

def printInLineProgressBar(
    iteration       : int, 
    len_of_iterable : int,
    label           : str = 'Processing: ',
    bar_width       : int = 40,
    # additional_text : str = None, 
):
    """
    Function which enables printing an inline progress bar. Which looks like
    this:
    Processing:  | [........................................] 100% [336 | 336]

    Place this function within a loop and provide at least the non default
    function arguments.

    Args:
        iteration (int): Number of iteration which is currently processed.
        len_of_iterable (int): The length of the iterable object (e.g. list)
        label (str, optional): 
            Any string you want for describing your loop. 
            Defaults to 'Processing: '.
        bar_width (int, optional): 
            Number, which defines the width of the progress bar itself. 
            Defaults to 40, which is a reasonable length to not exceed the 
            80 character limitation in the terminal.
    """


    j = (iteration + 1) / len_of_iterable
    sys.stdout.write('\r')
    bar = '.' * int(bar_width * j) # bisher geladen
    bar = bar + '-' * int(bar_width * (1-j)) # platzhalter bis 100%

    progress_bar = f"{label} | [{bar:{bar_width}s}] {int(100 * j)}% [{iteration+1} | {len_of_iterable}]"
    
    # if additional_text:
    #     progress_bar += '\n'
    #     progress_bar += additional_text
    
    sys.stdout.write(progress_bar)
    sys.stdout.flush()
    
    # print an empty line, if the iteration reached the end: ----------------- #
    if iteration + 1 ==  len_of_iterable:
        print()

def knowledgeHubLogoPrint():
    print(f'''
    
                                                                                    
                                        @@@#                                      
                                    @@@@@   .@@@@*                                 
                                @@@           (@@                                
                                #@@              @@                               
                                @@@              @@,                              
                                @@             @@@                               
                                    @@@         /@@@                                
                                    /@@@@@@@@@@                                   
                                        @@                                       
        .@@@@@@@@,                        @@                         .((((((((     
    ,@@@        @@@,                     @@                      *(((        (((  
    @@@            @@@                /@@@@@@@@,                 ((/            (((
    #@@              @@/          ,@@@@,        #@@@@            (((              ((
    *@@              @@*        @@@                 /@@@         /((              ((
    @@@            @@@@@@@&  @@@                      @@    @@@@@(((            ((/
    @@@%      %@@@       ,@@@                        @@@@        (((,      /(((  
        &@@@@@@%           @@                          @@            /((((((*     
                            *@@                          @@                         
                            @@                         .@@                         
                            &@@                        @@                          
                            ,@@                     &@@                           
                                @@@&                @@@.                            
                                @@@@@@@@(      %@@@@#%@@                            
                            @@#       .#@@@@(        /@@                          
                #@@@@@@@@@@@*                          .@@   @@@@@@@              
                @@@         @@@                            @@@@      .@@@%          
            /@@             @@@                         @@,           #@@         
            @@.              @@                        @@              (@@        
            @@@             /@@                        @@              *@@        
            @@@           @@@                         ,@@             @@         
                @@@@.    @@@@                             @@@#       %@@@          
                    &@@@@                                    @@@@@@@@@             

    ''')