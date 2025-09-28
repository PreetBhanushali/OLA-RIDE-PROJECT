Power BI Template Assets
========================

Files in this package:
- powerquery_m.txt        -> Power Query M scripts to load CSVs (uses a 'DataFolder' parameter)
- dax_measures.txt        -> Recommended DAX measures to create in the model
- theme.json              -> Power BI theme JSON (colors/styles)
- dashboard_screenshots/  -> the reference PNGs you provided (visual layout)
- database_schema.png     -> database schema image

How to create a .pbit Power BI Template using these assets
---------------------------------------------------------
1. Open Power BI Desktop.
2. Create a new report (File -> New).
3. Create a new parameter:
   - Home -> Manage Parameters -> New Parameter
   - Name: DataFolder
   - Type: Text
   - Suggested Values: Any value
   - Default Value: (set to the folder path where your CSV files are stored, e.g. C:\Users\You\data\)
4. Get Data -> Blank Query -> Advanced Editor.
   - Open powerquery_m.txt and copy the Ola(...) query you need OR paste the full file's content.
   - Replace the top-level call with something like: Ola(DataFolder) to create a query that reads the CSV.
   - For each table (VehicleTypes, BookingStatus, PaymentMethods, Locations) create a new blank query and call the respective function:
     - In Advanced Editor paste: = VehicleTypes(DataFolder) and then click Done. Rename query to vehicle_types.
     - Repeat for BookingStatus, PaymentMethods, Locations.
   - For the Ola main table: create a new query with: = Ola(DataFolder) and rename to ola_cleaned_dataset.
5. Close & Apply to load the data model.
6. In Model view, ensure relationships:
   - ola_cleaned_dataset[vehicle_type_id] -> vehicle_types[vehicle_type_id]
   - ola_cleaned_dataset[status_id] -> booking_status[status_id]
   - ola_cleaned_dataset[payment_method_id] -> payment_methods[payment_method_id]
   - ola_cleaned_dataset[pickup_location_id] -> locations[location_id]
   - ola_cleaned_dataset[drop_location_id] -> locations[location_id]
7. Create the DAX measures from dax_measures.txt in the Model view or in the report.
8. Import theme: View -> Themes -> Browse for theme.json
9. Build pages similar to the screenshots in the dashboard_screenshots folder:
   - Use Buttons + Bookmarks to create the left navigation bar.
   - Create the Vehicle Type page: Table visual with Vehicle Type, Total Booking Value, Success Booking Value, Avg Distance, Total Distance.
   - Create Overall, Revenue, Cancellation, Ratings pages using the measures and visuals described in the README.
10. Once report is finalized, save as a Power BI template:
    - File -> Export -> Power BI template (.pbit)
    - The .pbit will include queries and parameter definitions. When opened, users will be prompted to provide DataFolder.
