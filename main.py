import dempy

def main():

    api = dempy.DemAPI("http://localhost")

    """ Datasets """

    ## Get all datasets

    all_datasets = api.datasets.get()

    # or

    for dataset in api.datasets:
    	pass

    ## Get tagged datasets
    
    red_datasets = api.datasets.get(tags=["red"])

    ## Count datasets

    datasets_count = api.datasets.count()

    ## Create dataset

    dataset = api.datasets.create(dempy.Dataset(name = "Teste"))
    
    ## Get dataset

    api.datasets.id(dataset.id).get()

    ## Get dataset's acquisitions

    acquisitions = api.datasets.id(dataset.id).acquisitions.get()

    # or

    for acquisition in api.datasets.id(dataset.id).acquisitions:
        print(acquisition)

    ## Export dataset

    api.datasets.id(dataset.id).export(f"~/Desktop/{dataset.id}.zip")

    ## Delete dataset

    api.datasets.id(dataset.id).delete()

    """ Acquisitions """

    ## TODO

    """ Organizations """

    ## TODO

    """ Users """
    
    ## Get all users

    all_users = api.users.get()

    # or

    for user in api.users:
    	pass

    ## Count users

    users_count = api.users.count()

    ## Create user

    user = api.users.create(dempy.User(firstName = "Nome 1", lastName = "Nome 2"))

    ## Get user

    api.users.id(user.id).get()

    ## Delete user

    api.users.id(user.id).delete()
  
if __name__	== "__main__":
	main()
