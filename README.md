# pyCONAssistant

This module provides additional reporting capabilities to the ICON CMO accounting software.

To use this module, create a file called user.conf with the following contents:  
```
phone=[church phone number]  
user=[username]  
pass=[password]  
```

For example:  
```
phone=5555555555  
user=JoePUser  
pass=password  
```

## Libraries

### batchManager
The batchManager library contains functions that will display aggregated batch contributions.  

**displayGFContributionsByMonth()**  
This function will aggregate contribution batches by month number.  Only funds included in globals.GFList[] will be included in this total.  

**displayGFContributionsByBatch()**  
This function will aggregate contribution batches by batch entered date.  All funds except those listed in globals.FundsNotRecordedAtBank will be included in the total.
