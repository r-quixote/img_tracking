import sys

def update_progress_bar(progress, comment = None):
    """
    progress should be float 0 > 1
    https://stackoverflow.com/a/15860757/8254743
    output is of form:
    [#####--------------]
    """
    barLength = 40 ## Modify to change the length of the progress bar
    status = "working..."
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress == 1:
        status = "Done     "
    if progress > 1:
        status = "???OVER DONE???\r\n###############"
    block = int(round(barLength*progress))
    if comment == None:
        text = "\rPercent: [{0}] {1}% status: {2}".format( "#"*block + "-"*(barLength-block), "%.2f" %(progress*100), status)
    else:
        text = "\rPercent: [{0}] {1}% status: {2} comments: {3}".format("#"*block + "-"*(barLength-block), "%.2f" %(progress*100), status, comment)

    sys.stdout.write(text)
    sys.stdout.flush()

def update_progress_simple(progress, comment = None):
    """
    simple version
    progress should be float 0 > 1
    output is of form:
    12.31%
    """
    if isinstance(progress, int):
        progress = float(progress)

    sys.stdout.write("\r{}%".format("%.2f" %(progress*100)))
    sys.stdout.flush()



def update_progress_bar_fnacy(progress, start_time):
    """
    progress should be float 0 > 1
    https://stackoverflow.com/a/15860757/8254743
    output is of form:
    [#####--------------]
    """
    barLength = 40 ## Modify to change the length of the progress bar
    status = "working..."
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress > 1:
        status = "???OVER DONE???\r\n###############"
    block = int(round(barLength*progress))
    if progress>0:
        t_delt = time.perf_counter()-start_time
        comment = t_delt/progress
        t_left = comment-t_delt
        comment = time.strftime('%H:%M:%S', time.localtime(start_time+comment))
        t_left = int(t_left)

    else:
        comment = "--"
        t_left = "--"

    text = "\rPercent: [{0}] {1}% status: {2} total_estimate: {3}, time left: {4}".format("#"*block + "-"*(barLength-block), "%.2f" %(progress*100), status, comment, t_left)

    sys.stdout.write(text)
    sys.stdout.flush()




# =============================================================================
#
#     if perc >0:
#         delt = time.perf_counter() - t
#         estimate = (delt/perc) - delt
#         estimate = int(estimate)
#         if estimate > 70:
#             estimate = str(int(estimate/60))+" min"
#         else: estimate = str(estimate) + " sec"
#         progress_bar.update_progress_bar(perc, " time left ~ " + estimate)
# =============================================================================
