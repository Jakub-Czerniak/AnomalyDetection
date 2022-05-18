#include <iostream>
#include <fstream>
#include <string>

using namespace std;

//* Podział CSV na oddzielne pliki, nazwa pliku = $id_czujnika + ".txt"
// Do dzialania potrzebny jest utworzony folder o nazwie data
void separate_data(ifstream& data_file)
{
    int id, old_id; 
    string file_name;
    string text; 
    char c; 

    ofstream new_file;

    data_file >> id;

    while (!data_file.eof())
    {
        file_name = "./data/" + to_string(id) + ".txt"; // tutaj tworzona jest nazwa pliku z danymi
        new_file.open(file_name);
        new_file << "date; data" << endl;

        do
        {
            old_id = id;
            data_file >> c;
            getline(data_file,text);
            new_file << text << endl;

            data_file >> id;
        } while (old_id == id && !data_file.eof());

        new_file.close();
    }

    new_file.close();
}

int main(void)
{
    ifstream data_file("./Budynek_1_woda_historia.csv"); // tutaj wybierany jest plik, z ktorego czytamy
    separate_data(data_file);
}